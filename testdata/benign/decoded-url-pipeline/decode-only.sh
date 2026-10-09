#!/bin/sh
curl -s "$(echo 'aHR0cHM6Ly9leGFtcGxlLm9yZy9kYXRh' | openssl base64 -d -A)" > data.json
