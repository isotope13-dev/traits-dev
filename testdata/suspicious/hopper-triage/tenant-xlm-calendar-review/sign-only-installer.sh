#!/bin/zsh
curl -fsSL https://example.org/release.tar.gz -o /tmp/package.tar.gz
tar -xzf /tmp/package.tar.gz -C /tmp
xattr -cr /tmp/Example.app
codesign --force --deep --sign - /tmp/Example.app
open /tmp/Example.app
