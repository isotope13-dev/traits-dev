import hashlib
raw = b"test"
digest = hashlib.sha256(raw).hexdigest()
proof = {}
values = globals().get("EXTENDED_CVES", [])
warning = "For authorized penetration testing only"
