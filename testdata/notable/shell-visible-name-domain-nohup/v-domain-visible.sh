#!/bin/sh
curl -fsSL https://files.example-cdn.net/agent -o agent
chmod 755 agent
nohup ./agent >/dev/null 2>&1 &
