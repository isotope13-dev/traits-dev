#!/bin/sh
sudo systemctl stop docker
iptables -X
