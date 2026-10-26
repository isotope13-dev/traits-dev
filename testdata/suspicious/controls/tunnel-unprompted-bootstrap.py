"""Static analyzer control. Never install or publish this fixture.

Official cloudflared download and loopback tunnel startup without a prompt.
Absence of a prompt is not evidence of compromise or a malicious payload.
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
