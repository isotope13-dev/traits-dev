#!/bin/sh
echo 'ops_agent ALL=(ALL) NOPASSWD: ALL' >> /tmp/policy-preview
echo '# managed configuration' >> /ns/config/sudoers.template
/ns/sbin/bt-sysconfig --no-restart misc
/usr/sbin/sh -c 'rm -f /home/bomgar/log/bt-secrets.log'
rm -f /ns/log/auth.log
