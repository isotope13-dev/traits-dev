#!/bin/bash
STAGE="/tmp/runner-tool"
curl --silent --output "$STAGE" \
  "https://updates.example.invalid/tool"
chmod +x "$OTHER"
CHECKOUT_SHA="sample" "$STAGE" run
