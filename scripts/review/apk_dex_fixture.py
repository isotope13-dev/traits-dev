"""Minimal DEX tables for a static builder-boolean regression; no execution."""
import hashlib
import struct
import zlib


def string_dex(value, referenced=True):
    """Minimal static method with an optional const-string use of its pool item."""
    owner, obj = 'LFixture;', 'Ljava/lang/Object;'
    strings = sorted({owner, obj, 'V', 'run', value})
    si = {s: i for i, s in enumerate(strings)}
    types = sorted([owner, obj, 'V'], key=si.get)
    ti = {s: i for i, s in enumerate(types)}
    sp, tp = 112, 112 + 4 * len(strings)
    pp, mp, cp = tp + 12, tp + 24, tp + 32
    dp = cp + 32
    data, offsets = bytearray(), []
    for s in strings:
        offsets.append(dp + len(data))
        # These controls use BMP text; preserve the DEX MUTF-8 NUL spelling.
        encoded = s.encode().replace(b'\0', b'\xc0\x80')
        data += uleb(len(s.encode('utf-16-le')) // 2) + encoded + b'\0'
    while (dp + len(data)) % 4:
        data.append(0)
    codeoff = dp + len(data)
    code = [0x001a, si[value], 0x000e] if referenced else [0x000e]
    data += struct.pack('<HHHHII', 1, 0, 0, 0, 0, len(code))
    data += struct.pack('<' + 'H' * len(code), *code)
    classdata = dp + len(data)
    data += b'\0\0\1\0' + uleb(0) + uleb(9) + uleb(codeoff)
    while (dp + len(data)) % 4:
        data.append(0)
    mapoff = dp + len(data)
    maps = [(0, 1, 0), (1, len(strings), sp), (2, 3, tp), (3, 1, pp),
            (5, 1, mp), (6, 1, cp), (0x2002, len(strings), offsets[0]),
            (0x2001, 1, codeoff), (0x2000, 1, classdata), (0x1000, 1, mapoff)]
    data += struct.pack('<I', len(maps))
    for kind, count, offset in sorted(maps, key=lambda row: row[2]):
        data += struct.pack('<HHII', kind, 0, count, offset)
    out = bytearray(dp) + data
    out[:8] = b'dex\n035\0'
    struct.pack_into('<IIII', out, 32, len(out), 112, 0x12345678, 0)
    struct.pack_into('<I', out, 52, mapoff)
    for at, count, offset in [(56, len(strings), sp), (64, 3, tp), (72, 1, pp),
                              (80, 0, 0), (88, 1, mp), (96, 1, cp),
                              (104, len(data), dp)]:
        struct.pack_into('<II', out, at, count, offset)
    for i, offset in enumerate(offsets):
        struct.pack_into('<I', out, sp + i * 4, offset)
    for i, name in enumerate(types):
        struct.pack_into('<I', out, tp + i * 4, si[name])
    struct.pack_into('<III', out, pp, si['V'], ti['V'], 0)
    struct.pack_into('<HHI', out, mp, ti[owner], 0, si['run'])
    struct.pack_into('<IIIIIIII', out, cp, ti[owner], 1, ti[obj], 0, 0xffffffff, 0, classdata, 0)
    out[12:32] = hashlib.sha1(out[32:]).digest()
    struct.pack_into('<I', out, 8, zlib.adler32(out[12:]) & 0xffffffff)
    return bytes(out)

def uleb(n):
    out = bytearray()
    while True:
        v = n & 127
        n >>= 7
        out.append(v | (128 if n else 0))
        if not n:
            return out

def job_dex(value=None):
    owner = 'Landroid/app/job/JobInfo$Builder;'
    fixture = 'LFixture;'
    strings = sorted({owner, fixture, 'Ljava/lang/Object;', 'V', 'Z', 'VL', 'LZ', 'run', 'setPersisted'})
    si = {s: i for i, s in enumerate(strings)}
    types = sorted([owner, fixture, 'Ljava/lang/Object;', 'V', 'Z'], key=si.get)
    ti = {s: i for i, s in enumerate(types)}
    protos = sorted([('V', (owner,), 'VL'), (owner, ('Z',), 'LZ')], key=lambda p: (ti[p[0]], tuple((ti[v] for v in p[1]))))
    pi = {(p[0], p[1]): i for i, p in enumerate(protos)}
    methods = sorted([(fixture, 'run', pi['V', (owner,)]), (owner, 'setPersisted', pi[owner, ('Z',)])], key=lambda m: (ti[m[0]], si[m[1]], m[2]))
    mi = {m[1]: i for i, m in enumerate(methods)}
    sp = 112
    tp = sp + 4 * len(strings)
    pp = tp + 4 * len(types)
    mp = pp + 12 * len(protos)
    cp = mp + 8 * len(methods)
    dp = cp + 32
    data = bytearray()

    def align():
        while (dp + len(data)) % 4:
            data.append(0)
    offsets = []
    for s in strings:
        offsets.append(dp + len(data))
        data += uleb(len(s))
        data += s.encode() + b'\x00'
    param_offsets = []
    for _, params, _ in protos:
        align()
        param_offsets.append(dp + len(data))
        data += struct.pack('<I', len(params))
        data += b''.join((struct.pack('<H', ti[p]) for p in params))
    align()
    codeoff = dp + len(data)
    # v1 is the incoming builder; v0 carries the boolean argument.
    code = [0x000e] if value is None else [value << 12 | 0x0012, 0x206e, mi['setPersisted'], 0x0001, 0x000e]
    data += struct.pack('<HHHHII', 2, 1, 2, 0, 0, len(code)) + struct.pack('<' + 'H' * len(code), *code)
    classdata = dp + len(data)
    data += b'\x00\x00\x01\x00' + uleb(mi['run']) + uleb(9) + uleb(codeoff)
    align()
    mapoff = dp + len(data)
    maps = [(0, 1, 0), (1, len(strings), sp), (2, len(types), tp), (3, len(protos), pp), (5, len(methods), mp), (6, 1, cp), (8194, len(strings), offsets[0]), (4097, len(protos), param_offsets[0]), (8193, 1, codeoff), (8192, 1, classdata), (4096, 1, mapoff)]
    maps.sort(key=lambda r: r[2])
    data += struct.pack('<I', len(maps))
    for typ, n, off in maps:
        data += struct.pack('<HHII', typ, 0, n, off)
    out = bytearray(dp) + data
    out[:8] = b'dex\n035\x00'
    struct.pack_into('<IIII', out, 32, len(out), 112, 0x12345678, 0)
    struct.pack_into('<I', out, 52, mapoff)
    for at, n, off in [(56, len(strings), sp), (64, len(types), tp), (72, len(protos), pp), (80, 0, 0), (88, len(methods), mp), (96, 1, cp), (104, len(data), dp)]:
        struct.pack_into('<II', out, at, n, off)
    for i, off in enumerate(offsets):
        struct.pack_into('<I', out, sp + i * 4, off)
    for i, t in enumerate(types):
        struct.pack_into('<I', out, tp + i * 4, si[t])
    for i, (ret, params, shorty) in enumerate(protos):
        struct.pack_into('<III', out, pp + i * 12, si[shorty], ti[ret], param_offsets[i])
    for i, (cl, name, proto) in enumerate(methods):
        struct.pack_into('<HHI', out, mp + i * 8, ti[cl], proto, si[name])
    struct.pack_into('<IIIIIIII', out, cp, ti[fixture], 1, ti['Ljava/lang/Object;'], 0, 0xffffffff, 0, classdata, 0)
    out[12:32] = hashlib.sha1(out[32:]).digest()
    struct.pack_into('<I', out, 8, zlib.adler32(out[12:]) & 0xffffffff)
    return bytes(out)
