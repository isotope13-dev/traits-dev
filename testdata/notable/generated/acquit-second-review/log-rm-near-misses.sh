#!/bin/sh
# rm -f /ns/log/auth.log
printf '%s\n' 'rm -f /ns/log/auth.log'
cat /ns/log/auth.log
rm -f /ns/log/auth.log.1
rm -f /ns/log/auth.log.backup
