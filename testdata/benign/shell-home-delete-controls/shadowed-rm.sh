#!/bin/sh
rm() { printf 'preview: %s\n' "$*"; }
rm -rf "$HOME/Documents" "$HOME/Desktop" "$HOME/Pictures"
