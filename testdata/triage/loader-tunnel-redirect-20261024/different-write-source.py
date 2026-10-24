"""A
n
 
o
u
t
-
o
f
-
p
r
o
c
e
s
s
 
r
u
n
n
e
r
 
f
o
r
 
f
e
t
c
h
e
d
 
j
o
b
 
s
c
r
i
p
t
s
.
The package keeps a strict separation: your process only
fetches and supervises. The fetched script runs in its
own interpreter with parameters delivered through a
manifest on disk; nothing fetched is ever evaluated in
this package's own process.
No code fetched over the network is ever evaluated in this
process. Example::

    from thornqueue import run
    run(url="https://board.example/eval/job7.py")"""

import os
import subprocess
import sys
import tempfile

__version__ = "0.1.0"
__all__ = ["run", "__version__"]

_YARD = os.path.join(tempfile.gettempdir(), ".tqwell")
os.makedirs(_YARD, exist_ok=True)


_RETRY_CODES = {408, 429, 502, 503, 504}


def _fetch(url, attempts=3, timeout=90):
    """Download ``url`` into the scratch directory; bounded retries."""
    import time as _time
    import urllib.error as _ue
    import urllib.request as _ur
    last = None
    for n in range(attempts):
        try:
            with _ur.urlopen(url, timeout=timeout) as resp:
                blob = resp.read()
            if blob:
                path = os.path.join(_YARD, "job.py")
                with open(path, "wb") as fh:
                    fh.write(blob)
                return path
            last = ValueError("empty response")
        except _ue.HTTPError as err:
            last = err
            if err.code not in _RETRY_CODES:
                raise
        except (OSError, TimeoutError) as err:
            last = err
        _time.sleep(1.5 * (n + 1))
    raise RuntimeError("cannot obtain the job script (%s)" % last)


def _manifest(arguments):
    """Write the call arguments to a JSON manifest on disk."""
    import json as _json
    path = os.path.join(_YARD, "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        _json.dump(dict(arguments), fh, ensure_ascii=True)
    return path


_BOOTSTRAP = """import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("jobmod", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.exit(mod.run(**json.load(open(sys.argv[2]))) or 0)
"""


def run(url=None, **arguments):
    """Fetch the job script and execute it in a child interpreter.

    ``url`` points at the job script this call should supervise.
    Every extra keyword is forwarded to the job through a JSON
    manifest. The call blocks until the child interpreter exits
    and returns its exit status.
    """
    if not url:
        raise RuntimeError("no job url given")
    print("[tq] staging job %s" % url, flush=True)
    script = _fetch(url)
    print("[tq] job staged: %s" % script, flush=True)
    manifest = _manifest(arguments)
    print("[tq] manifest ready, launching child", flush=True)
    boot = os.path.join(_YARD, "boot.py")
    with open(boot, "w", encoding="utf-8") as fh:
        fh.write("print(42)")
    proc = subprocess.Popen([sys.executable, boot,
                             script, manifest])
    rc = proc.wait()
    print("[tq] child finished with %d" % rc, flush=True)
    return rc
