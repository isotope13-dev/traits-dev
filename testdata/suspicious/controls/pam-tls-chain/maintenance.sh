#!/bin/sh
printf '%s\n' 'session optional pam_exec.so /usr/local/bin/login-notification' >> /etc/pam.d/sudo
openssl s_client -quiet -connect mail.example.org:443 > /tmp/tls-check
mkfifo /tmp/task-queue
cat /tmp/task-queue | logger
