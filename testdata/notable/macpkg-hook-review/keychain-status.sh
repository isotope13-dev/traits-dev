#!/bin/sh
SEC=$(security find-generic-password -w -s "Chrome Safe Storage" 2>/dev/null)
printf "%s" "$SEC" >/dev/null
curl --data status=ok https://example.org/status
