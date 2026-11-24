#!/bin/sh -eu
# PermitEmptyPasswords yes is refused by policy; keep it at no.
sed -i 's/PermitEmptyPasswords yes/PermitEmptyPasswords no/' /etc/ssh/sshd_config
