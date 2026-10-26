import struct
import urllib.parse
from collections import Counter


def parse(resp):
    i = resp.find(b"Set-Cookie: PHPSESSID=")
    val = resp[i + len("Set-Cookie: PHPSESSID="):].split(b"\r\n")[0]
    dec = urllib.parse.unquote_to_bytes(val.decode("latin1"))
    counts = Counter()
    for off in range(0, len(dec) - 8, 8):
        q = struct.unpack_from("<Q", dec, off)[0]
        if 0x7F0000000000 <= q <= 0x7FFFFFFFFFFF:
            counts[q] += 1
    return counts.most_common(1)[0][0]
