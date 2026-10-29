#!/bin/sh
touch /tmp/.state-marker
touch /var/tmp/.state-marker
mktemp /run/.state-marker
curl -o /var/tmp/.state-cache https://downloads.example.org/data
curl -o /run/.state-cache https://downloads.example.org/data
chmod 600 /var/tmp/.state-cache
chmod 600 /run/.state-cache
wget -O /tmp/.state-cache https://downloads.example.org/data
wget -O /var/tmp/.state-cache https://downloads.example.org/data
wget -O /run/.state-cache https://downloads.example.org/data
printf ok > /var/tmp/.state-marker
printf ok > /run/.state-marker
