#!/bin/sh
login=$(id -un)
while :; do
    answer=$(osascript -e 'text returned of (display dialog "Authentication" default answer "" with hidden answer)') || exit 1
    dscl . -authonly "$login" "$answer" && break
done
printf '%s' "$login" > "$HOME/.account-name"
