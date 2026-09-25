"""Benign consent-gated tunnel bootstrap (remote-notebook helper shape).

Guards the consent-gated-vendor-tunnel-bootstrap exception: fetching the
tunnel vendor's own client from its official release endpoint, chmodding it,
pip-installing declared requirements, and launching it against a LOOPBACK
service URL after an explicit typed confirmation must stay below hostile.
Without the exception the urlretrieve+chmod+run and urlretrieve+pip-install
dropper composites misread this helper as a staged payload.
"""
import os
import subprocess
import sys
import urllib.request

TUNNEL_URL = (
    "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    "cloudflared-linux-amd64"
)


def main():
    if input("Authorize preparing approved jobs on this machine? Type YES: ").strip() != "YES":
        raise RuntimeError("Execution not authorized")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "jsonschema>=4,<5"],
        check=True,
    )
    binary = os.path.join(os.path.expanduser("~/helper"), "cloudflared")
    urllib.request.urlretrieve(TUNNEL_URL, binary)
    os.chmod(binary, 0o755)
    tunnel = subprocess.Popen(
        [binary, "tunnel", "--url", "http://127.0.0.1:8765", "--no-autoupdate"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    return tunnel.pid


if __name__ == "__main__":
    raise SystemExit(main())
