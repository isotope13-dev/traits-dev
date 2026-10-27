#!/bin/sh
if [ -f /tmp/enrolled ]; then
 curl -fsSL https://example.org/script | sh
fi
