"""Variant: ranges-file only (no LDAP), renamed identifiers, ssock receiver,
/sdk/vimServiceVersions.xml fingerprint form."""

import ipaddress
import socket
import ssl

import requests


def probe(ip):
    with socket.socket() as s:
        s.settimeout(2)
        if s.connect_ex((str(ip), 902)) != 0:
            return False
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with socket.create_connection((str(ip), 443), timeout=3) as raw:
        with ctx.wrap_socket(raw, server_hostname=str(ip)) as ssock:
            peer = ssock.getpeercert()
    if "vmware" not in str(peer).lower():
        return False
    r = requests.get(f"https://{ip}/sdk/vimServiceVersions.xml",
                     verify=False, timeout=5)
    return "VMware" in r.text


def main():
    with open("ranges.txt") as fh:
        nets = [ipaddress.ip_network(x.strip()) for x in fh if x.strip()]
    for net in nets:
        for ip in net.hosts():
            if probe(ip):
                print("hypervisor:", ip)


if __name__ == "__main__":
    main()
