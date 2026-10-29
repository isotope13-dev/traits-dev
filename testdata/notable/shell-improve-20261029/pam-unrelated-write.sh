#!/bin/sh
printf '%s\n' 'session optional pam_exec.so /tmp/session-helper'
printf '%s\n' '# policy documentation' >> /etc/pam.d/sshd
