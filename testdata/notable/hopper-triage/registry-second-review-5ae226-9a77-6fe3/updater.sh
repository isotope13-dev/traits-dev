#!/bin/bash
STAGE="/tmp/runner-tool"
curl --silent --output "$STAGE" \
  "https://updates.example.invalid/tool"
chmod +x "$STAGE"
CHECKOUT_SHA="sample" "$STAGE" run
