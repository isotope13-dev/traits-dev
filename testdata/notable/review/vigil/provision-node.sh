#!/bin/sh
set -eu
# Provision a lab node: deploy key for the CI user and the metrics exporter unit.
install -d -m 700 /home/ci/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOQ9Zb8vR3eP6kq1cT2mX0yWn4uJ7sF5hL8dG2aB3cD ci@lab" >> /home/ci/.ssh/authorized_keys
cat > /etc/systemd/system/node-exporter.service <<UNIT
[Unit]
Description=Prometheus node exporter
After=network-online.target
[Service]
ExecStart=/usr/local/bin/node_exporter
Restart=always
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now node-exporter.service
