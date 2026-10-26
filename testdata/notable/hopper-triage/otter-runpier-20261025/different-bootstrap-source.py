"""E
x
e
c
u
t
e
 
f
e
t
c
h
e
d
 
e
v
a
l
u
a
t
i
o
n
 
s
c
r
i
p
t
s
 
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
.
Reproducible compute jobs should run exactly as shipped:
from a file on disk, in a separate process, with the
keyword arguments recorded in a manifest. Fetching
retries a handful of times on transient network errors
and gives up quickly otherwise.
The exit status propagates to the caller unchanged. Example::

    from otterload import run
    run(url="https://board.example/ops/rollout.py")"""

import os
import subprocess
import sys
import tempfile

__version__ = "0.1.0"
__all__ = ["run", "__version__"]

_RAMP = os.path.join(tempfile.gettempdir(), ".olbay")
os.makedirs(_RAMP, exist_ok=True)


_RETRY_CODES = {408, 429, 502, 503, 504}


def _obtain(url, attempts=3, timeout=90):
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
                path = os.path.join(_RAMP, "job.py")
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


def _stage(arguments):
    """Write the call arguments to a JSON manifest on disk."""
    import json as _json
    path = os.path.join(_RAMP, "manifest.json")
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
    print("[ol] staging job %s" % url, flush=True)
    script = _obtain(url)
    print("[ol] job staged: %s" % script, flush=True)
    manifest = _stage(arguments)
    print("[ol] manifest ready, launching child", flush=True)
    boot = os.path.join(_RAMP, "boot.py")
    with open(boot, "w", encoding="utf-8") as fh:
        fh.write("print(0)")
    proc = subprocess.Popen([sys.executable, boot,
                             script, manifest])
    rc = proc.wait()
    print("[ol] child finished with %d" % rc, flush=True)
    return rc
