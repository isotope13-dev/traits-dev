#!/bin/sh
# OpenBSD: enumerate swap lines, swapoff -a, zero the device.
SWAPDEV=$(awk '$3 == "swap" {print $1; exit}' /etc/fstab)
if [ -b "$OTHER" ] && [ -n "$SWAPDEV" ]; then
  swapoff -a
  dd if=/dev/zero of=$SWAPDEV bs=1m
fi
