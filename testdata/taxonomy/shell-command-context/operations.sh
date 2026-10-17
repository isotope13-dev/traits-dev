#!/bin/sh
fpm -s dir -t deb .
tracepath example.com
grep -o 'abc' /tmp/data
apt-get install example
yum install example
chattr +i /root/.ssh/authorized_keys
/tmp/systemd
/dev/shm/sshd
