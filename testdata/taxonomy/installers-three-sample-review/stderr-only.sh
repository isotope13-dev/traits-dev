#!/bin/sh
# Decoded output goes to tar; only errors go to /dev/null.
tail -n +100 "$0" | base64 -d 2>/dev/null | tar -xz -C "$DEST" 2>/dev/null
