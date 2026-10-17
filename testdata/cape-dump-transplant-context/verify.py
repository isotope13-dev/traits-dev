"""Transplanted-cert conclusions do not survive CAPE reconstruction.

Run: python3 testdata/cape-dump-transplant-context/verify.py <scratch-directory>

`cert-transplant-fake-upx-carrier` and `cert-transplant-file-walker-infector`
convict a dangling certificate directory paired with UPX section names or
with file-walker plus timestomp legs. A CAPE-reconstructed memory image
matches that shape innocently: the overlay certificate is not mapped into
memory so the cert directory dangles, unpacked code keeps UPX section
names, and CAPE adds a synthetic `.CAPE` section. Both composites therefore
exclude the CAPE-dump context.

Controls: the transplant-pattern positive (dangling cert, UPX pair,
file-walker, timestomp, no `.CAPE` section) must report both hostiles; the
same image with a `.CAPE` section must report neither.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = (
    'objectives/evasion/masquerade/trust::cert-transplant-fake-upx-carrier',
    'objectives/evasion/masquerade/trust::cert-transplant-file-walker-infector',
)

IMPORTS = [
    ('KERNEL32.dll', 'FindFirstFileA'),
    ('KERNEL32.dll', 'FindNextFileA'),
    ('KERNEL32.dll', 'FindClose'),
    ('KERNEL32.dll', 'SetFileTime'),
]
# Points beyond the end of the tiny fixture, like a memory image whose
# overlay certificate was never mapped.
DANGLING_CERT = (0x77ca8, 0x3590)


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(imports, sections, cert_dir=None):
    """Minimal PE32 with named sections, an import table, and a cert dir."""
    size_headers, file_align = 0x200, 0x200
    n_sec = len(sections)
    size_headers = align(0x80 + 4 + 20 + 224 + n_sec * 40, file_align)
    rva, off = 0x1000, size_headers
    layout = []
    for name, blob, ch in sections:
        layout.append((name, rva, len(blob), off, ch, blob))
        rva += 0x1000
        off += align(len(blob), file_align)

    dlls = {}
    for dll, func in imports:
        dlls.setdefault(dll, []).append(func)
    imp = bytearray(0x200)
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
    assert cur <= 0x200, cur
    order = list(dlls.values())
    for i, (dll, funcs) in enumerate(dlls.items()):
        slot = ilt_off + sum((len(v) + 1) * 4 for v in order[:i])
        struct.pack_into('<IIIII', imp, i * 20, 0x2000 + slot, 0, 0,
                         0x2000 + dllname_off[dll], 0x2000 + slot)
        for j, fn in enumerate(funcs):
            struct.pack_into('<I', imp, slot + j * 4,
                             0x2000 + entries[(dll, fn)])
            o = entries[(dll, fn)]
            imp[o:o + 2] = b'\x00\x00'
            imp[o + 2:o + 2 + len(fn)] = fn.encode('ascii')
    for dll, o in dllname_off.items():
        imp[o:o + len(dll)] = dll.encode('ascii')

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, n_sec, 0, 0, 0, 224, 0x2102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<III', opt, 28, 0x400000, 0x1000, file_align)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0, 0x4000, size_headers)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    if cert_dir is not None:
        struct.pack_into('<II', opt, 96 + 4 * 8, *cert_dir)
    pe += bytes(opt)
    for name, vr, vs, fo, ch, blob in layout:
        pe += name.encode('ascii').ljust(8, b'\x00')
        body = bytes(imp) if name == 'UPX1' else blob
        pe += struct.pack('<IIIIIIHHI', vs, vr, align(len(body), file_align),
                          fo, 0, 0, 0, 0, ch)
    pe += b'\x00' * (size_headers - len(pe))
    for name, vr, vs, fo, ch, blob in layout:
        body = bytes(imp) if name == 'UPX1' else blob
        pe += body + b'\x00' * (align(len(body), file_align) - len(body))
    return bytes(pe)


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
    code = b'\x33\xc0\xc3' + b'\x90' * 100
    sections = [('UPX0', code, 0x60000020), ('UPX1', b'\x00' * 64, 0x40000040)]
    positive = dest / 'transplant-positive.exe'
    positive.write_bytes(build_pe(IMPORTS, sections, DANGLING_CERT))
    ids = scan(positive)
    for target in TARGETS:
        assert target in ids, ('positive must convict', target)
    print('PASS transplant-positive.exe', flush=True)

    negative = dest / 'cape-dump-negative.exe'
    negative.write_bytes(
        build_pe(IMPORTS, sections + [('.CAPE', b'\x00' * 64, 0x40000040)],
                 DANGLING_CERT))
    ids = scan(negative)
    for target in TARGETS:
        assert target not in ids, ('CAPE dump must be excluded', target)
    print('PASS cape-dump-negative.exe', flush=True)


if __name__ == '__main__':
    main()
