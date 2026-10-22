"""Construct an inert converter envelope for scanner controls."""
import hashlib
import struct


def build(seed=b"new seed", base=0x180000000):
    data = bytearray(0xA00)

    def put(offset, value, fmt="I"):
        struct.pack_into("<" + fmt, data, offset, value)

    data[:2] = b"MZ"
    put(0x3C, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    for offset, value in [(0x84, 0x8664), (0x86, 3), (0x94, 0xF0), (0x96, 0x22), (0x98, 0x20B), (0xDC, 2)]:
        put(offset, value, "H")
    put(0xB0, base, "Q")
    for offset, value in [(0xA8, 0x1000), (0xB8, 0x1000), (0xBC, 0x200), (0xD0, 0x4000), (0xD4, 0x200), (0x104, 16), (0x118, 0x3000), (0x11C, 0x400)]:
        put(offset, value)
    sections = [(b".renamed", 0x1000, 0x200, 0x200, 0x60000020),
                (b".values", 0x2000, 0x400, 0x200, 0xC0000040),
                (b".assets", 0x3000, 0x600, 0x400, 0x40000040)]
    for i, (name, rva, offset, length, flags) in enumerate(sections):
        header = 0x188 + 40 * i
        data[header:header + len(name)] = name
        for field, value in [(8, length), (12, rva), (16, length), (20, offset), (36, flags)]:
            put(header + field, value)
    data[0x200:0x211] = b"\x48\xb8" + struct.pack("<Q", base + 0x20A0) + b"\x48\x89\x05\0\0\0\0"
    data[0x4A0:0x4A8] = seed
    vocabulary = b"p2eincfilepath p2eincfilecount powershell"
    data[0x400:0x400 + len(vocabulary)] = bytes((-b) & 255 for b in vocabulary)
    for offset in [0x60E, 0x62E, 0x64E]:
        put(offset, 1, "H")
    for offset, value in [(0x610, 10), (0x614, 0x80000020), (0x630, 735), (0x634, 0x80000040), (0x650, 0), (0x654, 0x60), (0x660, 0x3080)]:
        put(offset, value)
    script = b"$message = 'ordinary application with no destructive behavior'; Write-Output $message\r\n"
    key = hashlib.md5(seed).hexdigest().upper().encode()
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 255
        s[i], s[j] = s[j], s[i]
    i = j = 0
    encrypted = bytearray()
    for b in script:
        i = (i + 1) & 255
        j = (j + s[i]) & 255
        s[i], s[j] = s[j], s[i]
        encrypted.append(b ^ s[(s[i] + s[j]) & 255])
    put(0x664, len(encrypted))
    data[0x680:0x680 + len(encrypted)] = encrypted
    return bytes(data)
