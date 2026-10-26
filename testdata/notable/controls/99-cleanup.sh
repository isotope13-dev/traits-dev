#!/bin/sh -eux
# Image-minimization cleanup: drop caches and truncate build-time logs so the
# shipped image is small. Truncating install-time logs here is hygiene, not
# anti-forensics.

apt-get -y autoremove;
apt-get -y clean;

# Remove docs
rm -rf /usr/share/doc/*

# Remove caches
find /var/cache -type f -exec rm -rf {} \;

# truncate any logs that have built up during the install
find /var/log -type f -exec truncate --size=0 {} \;

# Blank netplan machine-id (DUID) so machines get unique ID generated on boot.
truncate -s 0 /etc/machine-id
