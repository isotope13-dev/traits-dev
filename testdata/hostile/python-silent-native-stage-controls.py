"""Silent native stager control: fetches a versioned native wheel from
project releases and loads the extension. Manifest failures are swallowed
without any operator-visible warning, so verification degrades silently.
"""
import hashlib
import json
import os
import sys
import urllib.request
import zipfile

_BASE_URL = "https://github.com/example/widget/releases/download"


def _expected_sha256(tag):
    url = f"{_BASE_URL}/{tag}/widget-manifest.json"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
    except urllib.error.HTTPError:
        return None
    return json.loads(data).get("sha256")


def install(blob, dest, want):
    digest = _expected_sha256("v9")
    with zipfile.ZipFile(blob) as zf:
        for info in zf.infolist():
            if info.filename.endswith(".so"):
                with zf.open(info) as src, open(dest, "wb") as out:
                    out.write(src.read())
    import importlib.machinery
    loader = importlib.machinery.ExtensionFileLoader("widget._native", dest)
    return loader
