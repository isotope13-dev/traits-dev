#!/bin/sh
# Test fixture: ordinary per-architecture release installer (negative
# control). It selects an architecture and installs a release tarball, but
# never chmods 777, never detaches, and never touches a raw socket, so the
# multi-arch loader hostiles must stay silent.
set -e
M=$(uname -m)
case "$M" in
  x86_64) A=x86_64 ;;
  aarch64) A=aarch64 ;;
  *) echo "unsupported: $M" >&2; exit 1 ;;
esac
URL="https://releases.example.net/tool/$A/tool.tar.gz"
curl -fsSL "$URL" -o /tmp/tool.tar.gz
tar -xzf /tmp/tool.tar.gz -C /tmp
chmod +x tool-install
./tool-install --prefix "$HOME/.local"
