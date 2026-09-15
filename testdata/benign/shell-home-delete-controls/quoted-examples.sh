#!/bin/sh
# Documentation is data, not a command invocation.
printf '%s\n' 'rm -rf "$HOME/Documents" "$HOME/Desktop"'
cat <<'EXAMPLE'
    rm -rf "$HOME/Documents" "$HOME/Desktop" "$HOME/Pictures"
EXAMPLE
