"""CVE-2026-35273 probe with a fully percent-encoded PSEMHUB servlet path.

Regression fixture for the tightened PSEMHUB endpoint matcher: every
letter is required (plain or encoded), so partial tokens no longer match
while fully encoded spellings of the EMHub servlet still convict.
"""
import sys

import requests

target = sys.argv[1].rstrip("/")
payload = open(sys.argv[2], "rb").read()
response = requests.post(
    target + "/%50%53%45%4D%48%55%42/hub",
    data=payload,
    timeout=15,
)
print(response.status_code)
