#!/bin/sh
# One app-owned staging folder repeated is not distinct personal directories.
HOME=$(mktemp -d)
rm -rf "$HOME/Documents" "$HOME/Documents"
rmdir "$HOME"
