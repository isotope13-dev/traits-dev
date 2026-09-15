#!/bin/sh
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config
curl -sfL https://get.rke2.io | sh -
mkdir -p /etc/rancher/rke2
printf 'token: configured-token\n' > /etc/rancher/rke2/config.yaml
systemctl enable --now rke2-server.service
