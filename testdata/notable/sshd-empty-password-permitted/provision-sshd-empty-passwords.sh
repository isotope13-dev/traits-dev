#!/bin/sh -eu
# Build-image provisioning: allow passwordless SSH logins for the build user.
echo "PermitEmptyPasswords yes" >>/mnt/etc/ssh/sshd_config
run_root systemctl enable sshd
