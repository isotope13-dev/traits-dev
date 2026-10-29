#!/bin/sh
iptables -t filter -C OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP
iptables -t filter -D OUTPUT -p icmp -m icmp --icmp-type 3 -j DROP
