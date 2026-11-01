#!/bin/sh
echo 'ops_agent ALL=(ALL) NOPASSWD: ALL' >> /ns/config/sudoers.template
/ns/sbin/bt-sysconfig --no-restart misc
