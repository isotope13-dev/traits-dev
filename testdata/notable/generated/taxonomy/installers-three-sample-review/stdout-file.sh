#!/bin/sh
printf '%s' "$DATA" | base64 --decode > /tmp/output
