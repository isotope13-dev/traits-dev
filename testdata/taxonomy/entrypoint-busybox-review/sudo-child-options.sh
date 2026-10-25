#!/bin/sh
sudo lsof -n /dev/net/tun
sudo iotop -o -b -n 1
sudo /usr/bin/printf --non-interactive
