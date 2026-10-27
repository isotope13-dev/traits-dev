#!/bin/sh
cat /etc/ld.so.preload
printf "%s\n" "sudo tee /etc/ld.so.preload"
# sudo tee /etc/ld.so.preload
sudo rm -f /etc/ld.so.preload
