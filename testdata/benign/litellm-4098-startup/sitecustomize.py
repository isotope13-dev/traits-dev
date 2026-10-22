"""Site hook: warn when the pinned toolchain is older than the published one."""
import os
import sys

try:
    import requests
except ImportError:
    requests = None

INDEX = "https://pypi.org/pypi/acme-toolchain/json"


def _latest():
    resp = requests.get(INDEX, timeout=2)
    resp.raise_for_status()
    return resp.json()["info"]["version"]


def _check():
    if requests is None or os.environ.get("ACME_NO_VERSION_CHECK"):
        return
    try:
        latest = _latest()
    except Exception:
        return
    pinned = os.environ.get("ACME_TOOLCHAIN_VERSION", "")
    if pinned and pinned != latest:
        sys.stderr.write("acme-toolchain %s is available (pinned %s)\n" % (latest, pinned))


_check()
