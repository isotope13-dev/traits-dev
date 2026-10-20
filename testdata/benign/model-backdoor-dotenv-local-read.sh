#!/bin/sh
for config in .env .env.local; do
  cat "$PWD/$config"
done
curl -X POST https://collector.invalid/status -d 'ready'
