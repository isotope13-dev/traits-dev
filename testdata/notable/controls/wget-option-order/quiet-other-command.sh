#!/bin/sh
wget -O - https://example.invalid/tool.sh; printf '%s\n' -q
printf '%s\n' '$GOPATH_SUFFIX'
