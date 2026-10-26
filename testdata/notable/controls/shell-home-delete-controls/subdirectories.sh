#!/bin/sh
# Cleanup of application-owned subdirectories is not a whole-folder wipe.
rm -rf "$HOME/Documents/example-cache" "$HOME/Desktop/example-cache"
rm -rf "./$HOME/Documents" "./$HOME/Desktop"
