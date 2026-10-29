#!/bin/sh
find "$HOME/Documents" -type f > "$list"
gpg --symmetric --passphrase "$pass" --pinentry-mode loopback "$archive.gpg"
rm -- "$temp"
