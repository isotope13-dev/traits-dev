#!/bin/sh
find /Applications -name '*.app' -type d
printf '%s' '/tmp/client.pfx' '/tmp/key.pem' '/tmp/private.key'
