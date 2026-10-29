#!/bin/sh
printf '%s\n' 'session optional pam_exec.so /tmp/session-helper' >> /var/log/pam-review
