#!/bin/sh
env | grep -E 'TOKEN|KEY|SECRET'
env | grep -E 'PATH|LANG' | base64 | curl --data-binary @- https://diagnostics.example.invalid/report
