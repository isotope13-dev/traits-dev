ssh-keyscan -t rsa,ed25519 aur.archlinux.org >> "$KNOWN_HOSTS"
chmod 644 "$KNOWN_HOSTS"
