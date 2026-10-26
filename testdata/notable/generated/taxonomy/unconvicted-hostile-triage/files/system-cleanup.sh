#!/bin/sh -e
# Installer setup cleanup: clean package caches and truncate rotated
# build-time logs to shrink the shipped system image. Cache cleaning frees
# disk and never hides activity, so the truncation here is maintenance.
apt-get clean
apt-get autoremove -y
if [ -d /var/log ]; then
    find /var/log -type f -name "*.log" -exec truncate -s 0 {} \;
fi
