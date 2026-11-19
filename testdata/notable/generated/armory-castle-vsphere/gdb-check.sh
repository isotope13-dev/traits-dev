#!/bin/sh
echo IXByaW50ZiBvawpxCg== | base64 -d > /tmp/check.gdb
/usr/bin/gdb --pid=42 -x /tmp/check.gdb
