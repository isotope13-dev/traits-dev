#!/bin/sh
# OpenBSD: spaced dd operands still zero the swap device. The canonical
# variable-device trait must keep matching `of = $VAR`; only the spelling
# with spaces differs from 11-openbsd-swap.sh, not the behavior.
SWAPDEV=$(awk '/swap/ {print $1; exit}' /etc/fstab)
if [ -n "$SWAPDEV" ]; then
  swapoff -a
  dd if=/dev/zero of = $SWAPDEV bs=1m
fi
