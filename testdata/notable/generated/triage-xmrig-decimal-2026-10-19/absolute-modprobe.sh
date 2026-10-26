#!/bin/sh
/sbin/modprobe msr allow_writes=on > /dev/null 2>&1
MEM_DEVICE=/dev/mem
