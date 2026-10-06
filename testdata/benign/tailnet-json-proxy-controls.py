"""Tailnet-local JSON proxy control: posts the caller's own tool request to the
user's own Tailnet node (sk-access binds the tailnet IP, not loopback).
Shared address space (100.64.0.0/10) is not a public exfil endpoint.
"""
import json
import os
import urllib.request

_ACCESS_NODES = {
    ".158": "http://100.108.59.57:9386",
    ".41": "http://100.86.156.5:9386",
}

DEFAULT_HOSTD_URL = os.environ.get(
    "SKCODE_HOSTD_URL", "http://100.108.59.57:9394"
).rstrip("/")


def proxy_tool(node, token, tool, arguments):
    base = _ACCESS_NODES.get(node, _ACCESS_NODES[".158"])
    payload = json.dumps(
        {"token": token, "tool": tool, "arguments": arguments}
    ).encode()
    req = urllib.request.Request(
        f"{base}/tool",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()
