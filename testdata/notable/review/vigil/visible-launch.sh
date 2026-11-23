#!/bin/sh
setsid python3 /etc/agent.py >/dev/null 2>&1 &
printf ready >> /root/.bashrc
