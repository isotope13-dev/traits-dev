#!/bin/sh
# Isolated test-home setup/cleanup must not imply destruction of host data.
HOME=$(mktemp -d)
mkdir -p "$HOME/Documents" "$HOME/Desktop"
rm -rf "$HOME/Documents" "$HOME/Desktop"
rmdir "$HOME"
