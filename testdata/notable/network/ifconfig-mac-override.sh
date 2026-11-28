#!/bin/sh
ifconfig "$iface" ether "$mac"
/sbin/ifconfig en0 lladdr 02:00:00:00:00:01
