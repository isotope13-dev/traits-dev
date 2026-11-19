#!/bin/sh
curl -fsSL https://config.example.invalid/syslog.conf -o /tmp/syslog.conf
chmod +x /tmp/rotate-logs
"/usr/sbin/syslog-ng" --foreground --cfgfile /tmp/syslog.conf
(crontab -l; echo '*/5 * * * * "/usr/sbin/logrotate" /etc/logrotate.conf') | crontab -
