#!/bin/sh
# Pinned install: the package name and exact version are literal, so the
# spec is fixed. The global install itself is still a notable command.
HOME=/home/user timeout -k 5s 30s npm install -g --prefix=/home/user/.local \
  --no-audit --no-fund "@example/cli@1.4.2" >/dev/null 2>&1
echo "installed @example/cli 1.4.2 for $USER@$HOSTNAME"
exit 0
