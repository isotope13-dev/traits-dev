#!/bin/bash
# Near miss: vendor installer fetches its updater and registers a LaunchAgent,
# reports the hardware model, but performs no download-origin attribution.
MODEL=$(system_profiler SPHardwareDataType | awk '/Model Identifier/ {print $3}')
DEST="$HOME/Library/Application Support/ExampleSync"
PLIST="$HOME/Library/LaunchAgents/com.examplesync.updater.plist"
curl -fsSL "https://updates.examplesync.com/updater.zip" -o /tmp/es-updater.zip
ditto -x -k /tmp/es-updater.zip "$DEST"
defaults write "$PLIST" Label com.examplesync.updater
defaults write "$PLIST" Program "$DEST/Updater"
defaults write "$PLIST" RunAtLoad -bool true
launchctl load -w "$PLIST"
curl -fsS -d "model=$MODEL" https://updates.examplesync.com/installed
