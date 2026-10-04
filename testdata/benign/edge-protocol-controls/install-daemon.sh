#!/bin/sh
/bin/cp -f /opt/package/service /sbin/service
chmod 755 /sbin/service
/sbin/service &
