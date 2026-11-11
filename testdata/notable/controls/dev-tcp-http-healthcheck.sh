#!/bin/sh
# A small protocol health check uses Bash's direct socket path to issue HTTP.
exec 3<>/dev/tcp/example.com/80
printf 'GET /health HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n' >&3
cat <&3
