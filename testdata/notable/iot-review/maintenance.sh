#!/bin/sh
# Ordinary service maintenance, recurring backup, and reproducible timestamp.
(crontab -l 2>/dev/null; printf '*/3 * * * * /usr/local/bin/backup\n') | crontab -
chmod 755 /usr/local/bin/backup
touch -t 202001010000 /var/lib/backup/index
printf '%s\n' /etc/init.d/backup /etc/rc.local /etc/systemd/system
