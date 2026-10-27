#!/bin/sh
wget -O - -q https://example.invalid/tool.sh | sh -s -- -b "$GOPATH/bin"
