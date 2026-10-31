#!/bin/sh
# CI provisioning: the commands below remain observable even in a test path.
printf '%s' "$INPUT" | base64 -d | base64 -d > output.txt
