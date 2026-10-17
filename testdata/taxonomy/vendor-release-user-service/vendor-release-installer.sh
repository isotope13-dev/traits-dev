#!/bin/bash
bin_dir="$HOME/.local/bin"
url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
curl -fsSL -o "$bin_dir/cloudflared" "$url" || exit 1
[ -f "$bin_dir/cloudflared" ] && chmod +x "$bin_dir/cloudflared"
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/myapp.service" <<EOF
[Unit]
Description=My App Web Server
After=network-online.target

[Service]
Type=simple
ExecStart=$HOME/.local/bin/myapp-web
Restart=always

[Install]
WantedBy=default.target
EOF
systemctl --user enable myapp.service
