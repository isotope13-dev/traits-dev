#!/bin/sh
# A service-specific credential used by its own client is not browser theft.
TOKEN=$(security find-generic-password -w -s 'Example Status API' 2>/dev/null)
if [ -n "$TOKEN" ]; then
  printf '%s' "$TOKEN" | curl --data-binary @- https://status.example.invalid/authenticate
fi
