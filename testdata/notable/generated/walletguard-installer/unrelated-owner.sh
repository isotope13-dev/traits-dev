#!/bin/sh
PKG="walletguard-cli"
REPO="https://github.com/example/walletguard-cli.git"
if npm install -g "$PKG"; then
  exit 0
fi
