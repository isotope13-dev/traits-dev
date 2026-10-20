#!/bin/sh
curl --user "$2:$3" --data-urlencode 'wanMode=6' \
  --data-urlencode 'L2TPUserName=|id > /tmp/marker_l2tp #' \
  --data-urlencode 'submit-url=/wan.asp' "$1/goform/setWAN"
