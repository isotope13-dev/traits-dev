#!/bin/sh
# Static query-cost regression fixture; never execute these downloads.
# Retain the command that triggered the GitHub Actions run-block outlier,
# plus output-first, quoted, and combined-option variants.
curl -fsSL https://updates.example.invalid/data.json -o /tmp/.cache-data
curl --output .stage https://stage.invalid/bootstrap
curl -sfo '/tmp/.cache-data' 'https://updates.example.invalid/data.json'
curl -fsS --output ".stage" https://stage.invalid/bootstrap
