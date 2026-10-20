#!/bin/sh
curl --user "$2:$3" --data-urlencode 'wanMode=6' --data-urlencode 'L2TPUserName=guest@example.net' "$1/goform/setWAN"
