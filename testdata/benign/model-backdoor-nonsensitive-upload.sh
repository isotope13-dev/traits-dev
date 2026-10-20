#!/bin/sh
for log in build.log coverage.log; do
  curl "https://collector.invalid/log" -d "$(cat "$PWD/$log")"
done
