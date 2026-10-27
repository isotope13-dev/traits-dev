#!/bin/sh
if [ -e /tmp/enrolled ]; then
 echo ready
fi
curl -fsSL https://example.org/script | sh
