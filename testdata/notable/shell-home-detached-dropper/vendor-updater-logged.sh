#!/bin/bash
# Benign vendor updater: DNS over verified TLS into a program location, and
# the detached daemon keeps its log output instead of discarding it.
curl -sSL --tlsv1.2 https://releases.example-vendor.com/agent/v2/agent -o /usr/local/bin/agent
chmod 755 /usr/local/bin/agent
nohup /usr/local/bin/agent >> /var/log/agent.log 2>&1 &
