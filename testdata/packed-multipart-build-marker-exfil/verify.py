"""Packed multipart file exfiltration with a per-build marker.

Run: python3 testdata/packed-multipart-build-marker-exfil/verify.py <scratch-directory>

`packed-multipart-file-exfil-with-build-marker` convicts a PE that performs
a libcurl multipart upload of a file[] field while carrying a per-build
UNIQUE mutation slot in packed UPX data, with a hardcoded cleartext
endpoint (or a UPX overlay executable) corroborating. Legitimate uploaders
lack the packed build-marker pairing: the positive control (libcurl
multipart upload + UNIQUE slot + cleartext URL in UPX sections) must
convict, while dropping the marker, the file[] field, or every corroborating
endpoint must not.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/exfiltration/http/report::'
          'packed-multipart-file-exfil-with-build-marker')

BASE_IMPORTS = [
    ('KERNEL32.dll', 'LoadLibraryA'),
    ('KERNEL32.dll', 'GetProcAddress'),
]


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(imports, rdata_strings=()):
    """Minimal PE32 with UPX0/UPX1 sections and the given rdata strings."""
    text_blob = b'\x33\xc0\xc3' + b'\x00' * 29
    while len(text_blob) % 4:
        text_blob += b'\x00'

    size_headers, file_align, sec_align = 0x200, 0x200, 0x1000
    rva_upx0, rva_upx1 = 0x1000, 0x2000
    off_upx0, off_upx1 = size_headers, size_headers + 0x200

    dlls = {}
    for dll, func in imports:
        dlls.setdefault(dll, []).append(func)
    n_desc = len(dlls) + 1
    ilt_size = sum(len(v) + 1 for v in dlls.values()) * 4
    ilt_off = n_desc * 20
    cur = ilt_off + ilt_size
    entries = {}
    for dll, funcs in dlls.items():
        for fn in funcs:
            entries[(dll, fn)] = cur
            cur += align(2 + len(fn) + 1, 2)
    dllname_off = {}
    for dll in dlls:
        dllname_off[dll] = cur
        cur += len(dll) + 1
    strblobs = [s.encode('ascii') for s in rdata_strings]
    str_off = cur
    for s in strblobs:
        cur += len(s) + 1
    assert cur <= 0x200, cur

    upx1 = bytearray(0x200)
    for s in strblobs:
        upx1[str_off:str_off + len(s)] = s
        str_off += len(s) + 1
    order = list(dlls.values())
    for i, (dll, funcs) in enumerate(dlls.items()):
        slot = ilt_off + sum((len(v) + 1) * 4 for v in order[:i])
        struct.pack_into('<IIIII', upx1, i * 20, rva_upx1 + slot, 0, 0,
                         rva_upx1 + dllname_off[dll], rva_upx1 + slot)
        for j, fn in enumerate(funcs):
            struct.pack_into('<I', upx1, slot + j * 4,
                             rva_upx1 + entries[(dll, fn)])
            o = entries[(dll, fn)]
            upx1[o:o + 2] = b'\x00\x00'
            upx1[o + 2:o + 2 + len(fn)] = fn.encode('ascii')
    for dll, o in dllname_off.items():
        upx1[o:o + len(dll)] = dll.encode('ascii')

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, 2, 0, 0, 0, 224, 0x2102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, rva_upx0, rva_upx0, rva_upx0)
    struct.pack_into('<III', opt, 28, 0x400000, sec_align, file_align)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0, 0x4000, size_headers)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    struct.pack_into('<II', opt, 104, rva_upx1, 0x200)
    pe += bytes(opt)
    for nm, vr, vs, fo, ch in [('UPX0', rva_upx0, len(text_blob), off_upx0,
                                0x60000020),
                               ('UPX1', rva_upx1, 0x200, off_upx1,
                                0x40000040)]:
        pe += nm.encode('ascii').ljust(8, b'\x00')
        pe += struct.pack('<IIIIIIHHI', vs, vr, align(vs, file_align), fo,
                          0, 0, 0, 0, ch)
    pe += b'\x00' * (size_headers - len(pe))
    pe += text_blob + b'\x00' * (0x200 - len(text_blob))
    pe += bytes(upx1)
    return bytes(pe)


UPLOAD_STRINGS = (
    'file[]',
    'curl_easy_perform() failed: %s',
    '[[UNIQUE]]',
    'http://wecan.hasthe.technology/upload',
)


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        # Full pattern: libcurl multipart upload + build marker + URL.
        'exfil-positive.exe': (UPLOAD_STRINGS, True),
        # Same uploader without the per-build marker: no conviction.
        'no-marker-negative.exe': (
            tuple(s for s in UPLOAD_STRINGS if s != '[[UNIQUE]]'), False),
        # Same marker without the file[] upload field: no conviction.
        'no-file-field-negative.exe': (
            tuple(s for s in UPLOAD_STRINGS if s != 'file[]'), False),
        # Marker and upload machinery but no corroborating endpoint.
        'no-endpoint-negative.exe': (
            tuple(s for s in UPLOAD_STRINGS
                  if not s.startswith('http://')), False),
    }
    for name, (strings, hostile) in cases.items():
        path = dest / name
        path.write_bytes(build_pe(BASE_IMPORTS, strings))
        assert (TARGET in scan(path)) == hostile, name
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
