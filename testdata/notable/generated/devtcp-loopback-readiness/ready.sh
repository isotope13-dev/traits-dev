#!/bin/bash
for i in $(seq 1 100); do
  (exec 3<>/dev/tcp/127.0.0.1/8080) 2>/dev/null && break
  sleep 0.05
done
