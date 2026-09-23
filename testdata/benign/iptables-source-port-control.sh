#!/bin/sh
# Static fixture; a firewall rule mentioning --source-port is not a
# crafted-packet invocation. Guards the tool-name anchor on source-port.
iptables -I INPUT -p udp --destination-port 5002 -j ACCEPT
iptables -I OUTPUT -p udp --source-port 5002 -j ACCEPT
