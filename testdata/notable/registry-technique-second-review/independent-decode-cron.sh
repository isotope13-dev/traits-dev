#!/bin/sh
(crontab -l; echo '* * * * * /usr/local/bin/healthcheck') | crontab -
printf '%s' SGVsbG8K | base64 -d > /tmp/greeting
