#!/bin/sh
# Crypto miner configuration example; this file does not launch it.
WALLET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
POOL='example.org:3333'
PROTOCOL='stratum+tcp://example.org:3333'
chmod +x /tmp/public-report.sh
./public-report.sh
  mv /tmp/public-status /tmp/public-status.previous
