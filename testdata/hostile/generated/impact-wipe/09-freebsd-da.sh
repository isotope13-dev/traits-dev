#!/bin/sh
# FreeBSD disk wipe via geom + dd of da devices.
if [ "$(id -u)" -eq 0 ]; then
  geom disk list | awk '/Name:/{print "/dev/"$NF}' \
    | xargs -I{} dd if=/dev/zero of={} bs=1m
fi
