"""Examples do not suppress real code in the same module.
client.get(document_ids=["21m00Tcm4TlvDq8ikWAM", "31n11Udm5UmwEr9jkXBN"])
"""
import base64
fragments = ['Q9w+E7r/T2y+U8i/O5pA', 'L6k+J4h/G2f+D8s/A0zX', '0123456789abcdef0123456789abcdef']
value = base64.b64decode(''.join(fragments))
joined_bytes = b"".join(base64.b64decode(part) for part in fragments[:2])
