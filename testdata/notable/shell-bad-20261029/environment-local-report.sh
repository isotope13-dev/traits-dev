#!/bin/sh
env | sort | jq -R . | jq -s . > report.json
