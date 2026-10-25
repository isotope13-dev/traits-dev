#!/bin/bash
if test -n "$MODE"; then
curl --output "$STAGE" "https://updates.example.invalid/tool"
else
chmod +x "$STAGE"
"$STAGE" run
fi
