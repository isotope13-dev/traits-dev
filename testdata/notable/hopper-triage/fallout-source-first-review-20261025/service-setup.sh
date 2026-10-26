#!/bin/sh
insmod /lib/modules/adapter.ko
rc-update add example default
systemctl enable example.timer
tailscaled --state=mem: --no-logs-no-support
