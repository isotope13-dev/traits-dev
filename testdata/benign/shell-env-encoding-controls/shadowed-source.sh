#!/bin/sh
env() { printf 'KEY=public-status\n'; }
env | grep -E 'TOKEN|KEY|SECRET' | base64 | curl --data-binary @- https://diagnostics.example.invalid/report
