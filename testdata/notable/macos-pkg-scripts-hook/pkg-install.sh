#!/bin/sh
# macOS flat package installer step
PKG_ROOT="$1"
cp "$PKG_ROOT/Scripts/postinstall" /tmp/postinstall.sh
