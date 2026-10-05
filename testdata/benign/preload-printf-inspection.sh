#!/bin/sh
printf '%s\n' '/opt/appliance/lib/telemetry.so' '/opt/appliance/etc/ld.so.preload'
# printf '%s\n' '/opt/appliance/lib/telemetry.so' > '/opt/appliance/etc/ld.so.preload'
(crontab -l; printf '%s\n' '23 * * * * /usr/bin/true') | crontab -
