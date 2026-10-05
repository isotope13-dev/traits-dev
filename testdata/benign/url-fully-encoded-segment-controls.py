"""Benign control: a fully percent-encoded segment is ordinary escaping.

"/%41%42/health" carries no literal neighbour for the escape, so it is
not mixed literal+escaped over-encoding and must stay quiet on
objectives/evasion/security-bypass/waf.
"""
import sys

import requests

target = sys.argv[1].rstrip("/")
payload = open(sys.argv[2], "rb").read()
response = requests.post(
    target + "/%41%42/health",
    data=payload,
    timeout=15,
)
print(response.status_code)
