"""Benign control: authenticated vCenter inventory and certificate-expiry
monitoring for hosts the operator administers. TLS verification stays on;
hosts come from the vCenter inventory, not a subnet sweep."""

import socket
import ssl

import requests


def cert_expiry(host):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=5) as raw:
        with ctx.wrap_socket(raw, server_hostname=host) as ssock:
            return ssock.getpeercert()["notAfter"]


def inventory(vcenter, token):
    r = requests.get(f"https://{vcenter}/api/vcenter/host",
                     headers={"vmware-api-session-id": token}, timeout=10)
    r.raise_for_status()
    for host in r.json():
        name = host["name"]
        print(name, "cert expires", cert_expiry(name))
        s = requests.get(f"https://{name}/sdk/vimServiceVersions.xml",
                         timeout=10)
        print(" sdk status", s.status_code)
