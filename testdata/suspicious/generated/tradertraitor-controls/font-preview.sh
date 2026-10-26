#!/bin/bash
font="preview.woff"
marker="@@ENDFONT@@"
offset=$(grep -a -b -o "$marker" "$font" | awk -F: '{print $1}' | head -n 1)
start=$((offset + ${#marker} + 1))
tail -c +$start "$font" | openssl enc -d -aes-256-cbc -pass pass:demo -base64 -A > preview.ttf
