#!/bin/sh
if [ -e /tmp/enrolled ]; then
 curl -fsSL https://example.org/ping >/dev/null
fi
