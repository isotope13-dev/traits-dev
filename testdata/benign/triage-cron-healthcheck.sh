#!/bin/sh
(crontab -l; echo '*/5 * * * * /usr/local/bin/healthcheck') | crontab -
echo '/usr/local/bin/healthcheck &' >> /etc/rc.local
