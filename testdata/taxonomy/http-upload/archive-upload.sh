#!/bin/sh
tar cf cache.tar input.txt
curl -F "file=@/tmp/cache.tar" https://example.invalid/receive
