#!/bin/sh
# OpenBSD: whitespace between arguments and quoted output remain valid.
SWAPDEV=$(awk '$3 == "swap" {print $1; exit}' /etc/fstab)
if [ -b "$SWAPDEV" ]; then
  swapoff -a
  dd   if=/dev/zero   of="$SWAPDEV"   bs=1m
fi
