#!/bin/sh
# Cross-platform build helper: when running under WOW64, relaunch the
# Windows test step through the 32-bit command interpreter at
# C:\Windows\SysWOW64\cmd.exe instead of the 64-bit one.
SYSWOW64_CMD='C:\Windows\SysWOW64\cmd.exe'
echo "testing with $SYSWOW64_CMD"
