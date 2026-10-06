"""Static analyzer control. Never install or publish this fixture.

Minimal command-gated vendor tunnel bootstrap: the operator must type an
explicit install subcommand before anything is fetched.
"""
import os
import shutil
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


def dispatch(parts):
    if len(parts) > 1 and parts[1] in ("install", "download", "get"):
        binary = shutil.which("cloudflared") or _download_vendor_client()
        _start_tunnel(binary)


def main():
    dispatch(["tunnel", "install"])


main()
