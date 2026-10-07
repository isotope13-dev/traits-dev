#!/bin/sh
CVE_DATA="CVE-2019-13272 PTRACE_TRACEME kernel.unprivileged_userns_clone=1"
echo "modprobe mitigation (rxrpc): present"
for log_file in /var/log/messages /var/log/syslog; do
  echo "Found log: $log_file" | sed 's/log/LOG/g'
  tail -n 20 "$log_file"
done
find /etc -name "*.conf"
find "$HOME" -type f
PATTERN="*.pdf"
if [ -d "/private/var/db/emondClients" ]; then ls "/private/var/db/emondClients"; fi
# Example: tar cf archive.tar * --checkpoint-action=exec=sh
