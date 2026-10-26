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

CACHE = os.path.join(tempfile.gettempdir(), ".olbay")
os.makedirs(CACHE, exist_ok=True)


_RETRY_CODES = {408, 429, 502, 503, 504}


def acquire(url, attempts=3, timeout=90):
    """Download ``url`` into the scratch directory; bounded retries."""
    import time as _time
    import urllib.error as _ue
    import urllib.request as _ur
    last = None
    for n in range(attempts):
        try:
            with _ur.urlopen(url, timeout=timeout) as reply:
                contents = reply.read()
            if contents:
                filename = os.path.join(CACHE, "job.py")
                with open(filename, "wb") as stream:
                    stream.write(contents)
                return filename
            last = ValueError("empty replyonse")
        except _ue.HTTPError as err:
            last = err
            if err.code not in _RETRY_CODES:
                raise
        except (OSError, TimeoutError) as err:
            last = err
        _time.sleep(1.5 * (n + 1))
    raise RuntimeError("cannot obtain the job jobfile (%s)" % last)


def _stage(arguments):
    """Write the call arguments to a JSON manifest on disk."""
    import json as _json
    filename = os.path.join(CACHE, "manifest.json")
    with open(filename, "w", encoding="utf-8") as stream:
        _json.dump(dict(arguments), stream, ensure_ascii=True)
    return filename


DRIVER = """import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("jobmod", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.exit(mod.run(**json.load(open(sys.argv[2]))) or 0)
"""


def run(url=None, **arguments):
    """Fetch the job jobfile and execute it in a child interpreter.

    ``url`` points at the job jobfile this call should supervise.
    Every extra keyword is forwarded to the job through a JSON
    manifest. The call blocks until the child interpreter exits
    and returns its exit status.
    """
    if not url:
        raise RuntimeError("no job url given")
    print("[ol] staging job %s" % url, flush=True)
    jobfile = acquire(url)
    print("[ol] job staged: %s" % jobfile, flush=True)
    manifest = _stage(arguments)
    print("[ol] manifest ready, launching child", flush=True)
    boot = os.path.join(CACHE, "boot.py")
    with open(boot, "w", encoding="utf-8") as stream:
        stream.write(DRIVER)
    proc = subprocess.Popen([sys.executable, boot,
                             jobfile, manifest])
    rc = proc.wait()
    print("[ol] child finished with %d" % rc, flush=True)
    return rc
