#!/bin/bash
for i in $(seq 1 254); do
  (exec 3<>/dev/tcp/10.0.0.$i/22) 2>/dev/null && echo "10.0.0.$i open" && break
  sleep 0.05
done
