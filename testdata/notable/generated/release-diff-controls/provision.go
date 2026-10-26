package control
const setup = `set -euo pipefail
sudo tee /etc/sudoers.d/build-user >/dev/null <<EOF_SUDO
build-user ALL=(ALL) NOPASSWD: ALL
EOF_SUDO
sudo defaults write com.apple.network.local-network "$key" -array "10.0.0.0/8"
`
const plist = `<string>/var/log/build-agent.log</string>`
const install = `if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://example.org/install.sh)"
fi`
var kcpasswordKey = []byte{0x7d, 0x89}
// systemctl enable --now tailscaled is the Linux equivalent.
