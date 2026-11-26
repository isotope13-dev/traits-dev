#!/bin/bash
set -e
url=https://downloads.example.org/tool/darwin_arm64/tool
curl -fsSL -o tool "$url"
xattr -c tool
codesign --force --sign - tool
chmod +x tool
