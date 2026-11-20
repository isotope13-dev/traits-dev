#!/bin/sh
(crontab -l; echo '*/7 * * * * ls /proc/[0-9]*/cmdline 2>/dev/null | xargs -r grep -lFm1 -- worker >/dev/null 2>&1 || nohup /opt/worker >/dev/null 2>&1 &') | crontab -
