#!/bin/sh
wget -O - https://example.invalid/-q
printf '%s\n' "${GOPATH}/bin"
