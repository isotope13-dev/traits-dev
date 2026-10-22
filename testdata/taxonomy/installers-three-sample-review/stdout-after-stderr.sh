#!/bin/sh
printf '%s' "$DATA" | base64 -d 2>/dev/null > /tmp/output
