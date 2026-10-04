#!/bin/sh
/bin/cp -f /opt/package/worker /sbin/time-agent
chmod 755 /sbin/time-agent
/sbin/time-agent &
sleep 20
rm -rf /sbin/time-agent
/bin/cp -f /opt/package/helper /sbin/device-agent
chmod 755 /sbin/device-agent
/sbin/device-agent &
sleep 20
rm -rf /sbin/device-agent
