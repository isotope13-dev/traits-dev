#!/bin/sh
echo "operator ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
sudo -n bash /tmp/task.sh
