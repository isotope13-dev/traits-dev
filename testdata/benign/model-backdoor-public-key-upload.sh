#!/bin/sh
for key in id_rsa id_ed25519; do
  curl "https://collector.invalid/enroll" -d "$(cat "$HOME/.ssh/$key.pub")"
done
