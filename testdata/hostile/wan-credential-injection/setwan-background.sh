#!/bin/sh
curl --user "$2:$3" --data-urlencode 'wanMode=2' \
  --data-urlencode 'pppUserName=&id > /tmp/marker_bg #' \
  --data-urlencode 'submit-url=/wan.asp' "$1/goform/setWAN"
