import os, io, tarfile, urllib.request
from Crypto.Cipher import AES
def backup(src, url, key):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add(src, arcname="documents")
    raw = buf.getvalue()
    raw += b"\0" * (16 - len(raw) % 16)
    enc = AES.new(key, AES.MODE_CBC, iv=b"\0" * 16).encrypt(raw)
    req = urllib.request.Request(url, data=enc, method="POST")
    urllib.request.urlopen(req, timeout=60)
