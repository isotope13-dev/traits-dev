#!/usr/bin/env bash
# Controls for hosts-tee-overwrite: appending via tee -a, reading, and
# writing adjacent files must not match the overwrite pattern.
grep -v '^#' /etc/hosts | cat
sudo tee -a /etc/hosts < /tmp/extra-hosts
tee /etc/hosts.deny < /tmp/blocklist
cp /etc/hosts /mnt/backup/hosts
