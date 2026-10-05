#!/bin/sh
curl -fsS https://example.invalid/share --data-urlencode "selection=$(/usr/bin/pbpaste)"
