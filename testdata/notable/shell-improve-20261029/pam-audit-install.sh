#!/bin/sh
printf '%s\n' 'session optional pam_exec.so /usr/local/bin/session-audit' >> /etc/pam.d/sshd
