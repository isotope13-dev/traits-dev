#!/bin/bash
nsenter --net=/proc/123/ns/net -- tcpdump -i eth0
chisel client --auth "$user:$pass" "$server" R:8080:localhost:8080
curl -k -u "$user:$pass" "$bmc/redfish/v1/Systems"
