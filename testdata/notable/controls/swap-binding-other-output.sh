#!/bin/sh
# OpenBSD: enumerate swap lines, swapoff -a, zero the device.
SWAPDEV=$(awk '$3 == "swap" {print $1; exit}' /etc/fstab)
device=/tmp/cache
if [ -b "$SWAPDEV" ]; then
  swapoff -a
  dd if=/dev/zero of=$device bs=1m
fi
