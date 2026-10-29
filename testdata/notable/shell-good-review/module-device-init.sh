#!/bin/sh
# chkconfig: 345 28 72
modprobe autofs4
mknod -m 0600 /tmp/test-device c 10 235
