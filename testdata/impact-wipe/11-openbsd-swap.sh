#!/bin/sh
# OpenBSD: enumerate swap lines, swapoff -a, zero the device.
SWAPDEV=$(awk '/swap/ {print $1; exit}' /etc/fstab)
if [ -n "$SWAPDEV" ]; then
  swapoff -a
  dd if=/dev/zero of=$SWAPDEV bs=1m
fi
