#!/bin/zsh
curl -s https://updates.example.invalid/bootstrap > artifact
openssl base64 -e -A
xattr -l ./artifact
