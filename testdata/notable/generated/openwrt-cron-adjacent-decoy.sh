#!/bin/sh
echo 'backup enabled' > /etc/crontabs/root
echo '*/5 * * * * /usr/bin/backup' > /tmp/crontab
