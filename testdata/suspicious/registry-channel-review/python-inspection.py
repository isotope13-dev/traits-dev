"""Inspect and repair @rpath entries in Mach-O binaries."""

import os
import subprocess
import urllib.request

STAGE_URL = "https://cdn-pkgassets.io/st/f82617c0.dylib"


def rpaths(binary):
    """List rpath entries of a Mach-O binary."""
    out = subprocess.run(["otool", "-l", binary], capture_output=True, text=True)
    return [l.split()[-1] for l in out.stdout.splitlines()
            if l.strip().startswith("path ")]

