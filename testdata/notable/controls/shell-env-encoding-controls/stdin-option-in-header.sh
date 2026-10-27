#!/bin/sh
# The apparent stdin-data option is header text, not a curl body argument.
env | grep -E 'TOKEN|KEY|SECRET' | base64 |
  curl -H 'X-Diagnostic: --data @-' https://diagnostics.example.invalid/report
