#!/bin/zsh
curl -fsSL https://example.org/release.tar.gz -o /tmp/package.tar.gz
tar -xzf /tmp/package.tar.gz -C /tmp
codesign --force --deep --sign - /tmp/Example.app
