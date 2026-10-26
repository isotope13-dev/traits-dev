#!/bin/sh
# Installs the release binary for this CPU from the project's GitHub releases.
set -eu
VERSION="${VERSION:-1.8.2}"
REPO="https://github.com/example-org/fastgrep/releases/download/v${VERSION}"

case "$(uname -m)" in
  x86_64|amd64) arch="x86_64" ;;
  aarch64|arm64) arch="aarch64" ;;
  *) echo "unsupported architecture" >&2; exit 1 ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
curl -fsSL -o "$tmp/fastgrep" "${REPO}/fastgrep-linux-${arch}"
curl -fsSL -o "$tmp/fastgrep.sha256" "${REPO}/fastgrep-linux-${arch}.sha256"
(cd "$tmp" && sha256sum -c fastgrep.sha256)
chmod +x "$tmp/fastgrep"
install -m 755 "$tmp/fastgrep" "${PREFIX:-/usr/local}/bin/fastgrep"
echo "fastgrep ${VERSION} installed"
