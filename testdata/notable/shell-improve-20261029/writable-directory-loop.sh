#!/bin/sh
for dir in /tmp /var/tmp /root /etc; do
 test -w "$dir" && break
done
printf '%s\n' ELF | grep -q ELF
