#!/bin/sh
iptables -C INPUT -p tcp --tcp-flags RST RST -j DROP
iptables -C OUTPUT -p tcp --tcp-flags RST RST -j ACCEPT
iptables -C OUTPUT -p icmp --icmp-type 13 -j DROP
iptables -C OUTPUT -p tcp; printf '%s' '--tcp-flags RST RST -j DROP'
