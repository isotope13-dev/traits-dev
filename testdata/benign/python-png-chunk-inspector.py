"""Read PNG chunk lengths for a remote image inventory report."""

from urllib.request import urlopen
import struct

IMAGE = "https://images.example.org/samples/chart.png"
blob = urlopen(IMAGE).read()
offset = 8
chunk_types = []
while offset < len(blob):
    length = struct.unpack(">I", blob[offset:offset + 4])[0]
    kind = blob[offset + 4:offset + 8]
    if kind == b"IDAT":
        chunk_types.append("image-data")
    chunk_types.append(kind.decode("ascii", "replace"))
    if kind == b"IEND":
        break
    offset += length + 12
