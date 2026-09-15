#!/bin/sh
SECRET=$(security find-generic-password -w -s 'Chrome Safe Storage' 2>/dev/null)
STATUS=$(printf 'ready')
if [ -n "$STATUS" ]; then
  printf '%s' "$STATUS" | curl --data-binary @- https://status.example.invalid/check
fi
