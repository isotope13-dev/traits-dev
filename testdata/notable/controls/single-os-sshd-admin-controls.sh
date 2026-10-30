#!/bin/sh
# Benign single-OS Linux server bootstrap enabling sshd after config check.
set -eu

if /usr/sbin/sshd -t; then
    systemctl enable --now sshd
fi
