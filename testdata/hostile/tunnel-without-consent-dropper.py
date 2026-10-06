"""Static analyzer control. Never install or publish this fixture.

Counterfactual to tunnel-install-consent-controls.py: identical bootstrap
with NO explicit install subcommand gating the download, so the
command-gated exception must not engage and the dropper composite fires.
"""
import os
import subprocess
import urllib.request

TUNNEL_TARGET = "http://127.0.0.1:9090"


def _download_vendor_client():
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    tmp = "/tmp/vendor-client.tmp"
    urllib.request.urlretrieve(url, tmp)
    os.chmod(tmp, 0o700)
    return tmp


def _start_tunnel(binary):
    return subprocess.Popen([binary, "tunnel", "--url", TUNNEL_TARGET])


def main():
    binary = _download_vendor_client()
    _start_tunnel(binary)


main()
