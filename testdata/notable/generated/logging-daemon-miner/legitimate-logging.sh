#!/bin/sh
/usr/sbin/syslog-ng --foreground --cfgfile /etc/syslog-ng/syslog-ng.conf
(crontab -l; echo '*/5 * * * * /usr/sbin/logrotate /etc/logrotate.conf') | crontab -
