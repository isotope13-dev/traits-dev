#!/bin/sh
PKG="walletguard-cli"
REPO="https://github.com/verifygmail2-debug/walletguard-cli.git"
if npm install -g "$PKG" --no-fund --no-audit; then
  exit 0
fi
