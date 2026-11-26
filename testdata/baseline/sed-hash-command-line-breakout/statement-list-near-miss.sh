#!/bin/sh
awk '{print $1}' "$SESSION/live_hosts.txt" | sed 's#^https\?://##; s#/.*##' | head -n 8
sed -e 's#x##' | sed -e 's#y##'
