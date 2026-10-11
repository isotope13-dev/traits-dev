#!/bin/sh
SWAPDEV=$(awk '$3 == "swap" {print $1; exit}' /etc/fstab)
swapoff -a
printf "%s\n" "$SWAPDEV"
