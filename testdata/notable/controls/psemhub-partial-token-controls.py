"""Benign control: a partial PSEMHUB-like token is not the EMHub servlet.

"/PHUB/hub" matched the old optional-letter endpoint matcher; the
tightened rule requires every PSEMHUB letter, so this file must stay
quiet on objectives/execution/exploit/deserialization.
"""
import sys

import requests

target = sys.argv[1].rstrip("/")
payload = open(sys.argv[2], "rb").read()
response = requests.post(
    target + "/PHUB/hub",
    data=payload,
    timeout=15,
)
print(response.status_code)
