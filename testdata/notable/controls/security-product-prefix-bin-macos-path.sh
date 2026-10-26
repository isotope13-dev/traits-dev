#!/bin/sh
BASE_URL="https://raw.githubusercontent.com/example/helpers/main"
FILES="c cdt exe! lock ns r su tc tct x"
printf "%s\n" 'chmod +x "$BIN_DIR/$cmd"'
curl -fsSL "$BASE_URL/helper.sh" -o /tmp/helper
printf "%s\n" /Library/Objective-See
