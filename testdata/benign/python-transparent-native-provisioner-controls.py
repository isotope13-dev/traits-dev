"""Integrity-degradation atom control (cf. a3s-code bootstrap).

Exercises the generalized technique atoms without assembling the loader
composite (no ExtensionFileLoader call on purpose): release-manifest fetch
with a network-error branch that returns no digest, a stderr warning on
the degradation path, and a documented SKIP_VERIFY opt-out switch.
"""
import json
import os
import sys
import urllib.request

_BASE_URL = "https://github.com/example/widget/releases/download"
SKIP_NOTE = "Override with WIDGET_SKIP_VERIFY=1 for hermetic offline mirrors."


def _skip_requested():
    return os.environ.get("WIDGET_SKIP_VERIFY", "") == "1"


def _expected_sha256(tag):
    url = f"{_BASE_URL}/{tag}/widget-manifest.json"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"widget: warning: manifest fetch failed ({exc}); skipping hash check\n")
        return None
    return json.loads(data).get("sha256")
