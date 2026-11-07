#!/bin/bash
# Attribution + fetched autostart agent without a hardware identifier leg.
REF=$(xattr -px com.apple.metadata:kMDItemWhereFroms "$1" | xxd -r -p | plutil -p - | grep -om1 'http[^"]*')
PUB=$(echo "$REF" | sed -e 's/.*pubid=\([[:alnum:]]*\).*/\1/')
APP="$HOME/Library/Application Support/QuickViewer"
LA="$HOME/Library/LaunchAgents/com.quickviewer.agent.plist"
curl --retry 3 -f "https://static.example-viewer.com/agent.zip" -o "/tmp/qv.zip"
ditto -x -k /tmp/qv.zip "$APP"
defaults write "$LA" Label com.quickviewer.agent
defaults write "$LA" Program "$APP/QuickViewerAgent"
defaults write "$LA" RunAtLoad -bool YES
launchctl load -w "$LA"
curl -s -d "pub=$PUB&event=done" https://events.example-viewer.com/pkg
