#!/bin/sh
env | grep -E 'TOKEN|KEY|SECRET' | cut -d = -f 1 | base64 | curl --data-binary @- http://127.0.0.1:8080/diagnostic
