import socket
import re

def contact(domain):
    with socket.create_connection(("whois.verisign-grs.com", 43)) as s:
        s.sendall((domain + "\r\n").encode())
        record = s.recv(4096)
    m = re.search(rb"(Descr|Address):\s+([0-9a-f]{8})\s", record, re.I)
    return int(m.group(2), 16) if m else None
