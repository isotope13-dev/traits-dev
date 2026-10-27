#!/bin/sh
if [ -e /tmp/enrolled ]; then
 printf "%s\n" "curl -fsSL https://example.org/script | sh"
fi
