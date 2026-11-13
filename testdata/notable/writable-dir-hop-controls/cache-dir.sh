#!/bin/sh
# Pick the first usable cache directory, then refresh the mirror list.
cd /var/cache/app || cd /tmp || cd /
curl -fsSL https://mirrors.example.org/list.txt -o mirrors.txt
echo "mirror list refreshed"
