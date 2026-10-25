#!/bin/bash
STAGE="/tmp/runner-tool"
curl --silent --output "$STAGE" \
  "file:///tmp/input"
chmod +x "$STAGE"
CHECKOUT_SHA="sample" "$STAGE" run
