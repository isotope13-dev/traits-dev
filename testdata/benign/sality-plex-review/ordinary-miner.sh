#!/bin/sh
# Explicit user-managed miner installation.
W="$HOME/xmrig"
mkdir -p "$W"
curl https://example.org/xmrig -o "$W/xmrig"
chmod 755 "$W/xmrig"
setsid "$RUN" --config "$W/config.json" --cpu-max-threads-hint=80
