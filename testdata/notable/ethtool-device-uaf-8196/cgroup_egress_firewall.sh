#!/bin/sh
set -eu

SERVICE_CGROUP="system.slice/nginx.service"
/usr/sbin/iptables -A OUTPUT -m cgroup --path "$SERVICE_CGROUP" -p tcp --dport 443 -j ACCEPT
/usr/sbin/iptables -A OUTPUT -m cgroup --path "$SERVICE_CGROUP" -j DROP
