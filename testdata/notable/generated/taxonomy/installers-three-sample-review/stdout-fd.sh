#!/bin/sh
printf '%s' "$DATA" | base64 -d 1>/tmp/output
