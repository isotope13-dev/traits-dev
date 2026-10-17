"""GUI framework libraries are not surveillance tools.

Run: python3 testdata/mfc-framework-hook-capture/verify.py <scratch-directory>

`persistent-keylogger-desktop-surveillance` combines GDI capture,
desktop-window access, hook lifecycle, registry writes and process
termination. Frameworks expose that surface as plumbing, so the composite
excludes catalogued libraries. The positive control (same API surface, no
framework marker) must still convict.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/collection/screenshot::'
          'persistent-keylogger-desktop-surveillance')

IMPORTS = [
    ('GDI32.dll', 'BitBlt'),
    ('GDI32.dll', 'GetDIBits'),
    ('USER32.dll', 'GetDesktopWindow'),
    ('USER32.dll', 'SetWindowsHookExA'),
    ('USER32.dll', 'CallNextHookEx'),
    ('USER32.dll', 'GetWindowTextA'),
    ('ADVAPI32.dll', 'RegSetValueExA'),
    ('ADVAPI32.dll', 'RegCreateKeyExA'),
    ('KERNEL32.dll', 'TerminateProcess'),
]
API_STRINGS = ['BitBlt', 'SetWindowsHookEx', 'CallNextHookEx',
               'TerminateProcess']


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(*, rdata_strings=()):
    """Minimal PE32 importing the hook/capture/registry/kill surface."""
    text_blob = b'\x33\xc0\xc3' + b'\x00' * 29
    for s in API_STRINGS:
        text_blob += s.encode('ascii') + b'\x00'
    while len(text_blob) % 4:
        text_blob += b'\x00'

    size_headers, file_align, sec_align = 0x200, 0x200, 0x1000
    rva_text, rva_rdata = 0x1000, 0x2000
    off_text, off_rdata = size_headers, size_headers + 0x200

    dlls = {}
    for dll, func in IMPORTS:
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
    str_off = cur
    for s in rdata_strings:
        cur += len(s.encode('ascii')) + 1
    assert cur <= 0x200, cur

    rdata = bytearray(0x200)
    for s in rdata_strings:
        rdata[str_off:str_off + len(s)] = s.encode('ascii')
        str_off += len(s) + 1
    order = list(dlls.values())
    for i, (dll, funcs) in enumerate(dlls.items()):
        slot = ilt_off + sum((len(v) + 1) * 4 for v in order[:i])
        struct.pack_into('<IIIII', rdata, i * 20, rva_rdata + slot, 0, 0,
                         rva_rdata + dllname_off[dll], rva_rdata + slot)
        for j, fn in enumerate(funcs):
            struct.pack_into('<I', rdata, slot + j * 4,
                             rva_rdata + entries[(dll, fn)])
            o = entries[(dll, fn)]
            rdata[o:o + 2] = b'\x00\x00'
            rdata[o + 2:o + 2 + len(fn)] = fn.encode('ascii')
    for dll, off in dllname_off.items():
        rdata[off:off + len(dll)] = dll.encode('ascii')

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, 2, 0, 0, 0, 224, 0x2102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, rva_text, rva_text, rva_text)
    struct.pack_into('<III', opt, 28, 0x400000, sec_align, file_align)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0, 0x4000, size_headers)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    struct.pack_into('<II', opt, 104, rva_rdata, 0x200)
    pe += bytes(opt)
    for nm, vr, vs, fo, ch in [('.text', rva_text, len(text_blob), off_text,
                                0x60000020),
                               ('.rdata', rva_rdata, 0x200, off_rdata,
                                0x40000040)]:
        pe += nm.encode('ascii').ljust(8, b'\x00')
        pe += struct.pack('<IIIIIIHHI', vs, vr, align(vs, file_align), fo,
                          0, 0, 0, 0, ch)
    pe += b'\x00' * (size_headers - len(pe))
    pe += text_blob + b'\x00' * (0x200 - len(text_blob))
    pe += bytes(rdata)
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

    positive = dest / 'hook-capture-positive.exe'
    positive.write_bytes(build_pe())
    assert TARGET in scan(positive), 'unmarked API surface must convict'
    print('PASS hook-capture-positive.exe', flush=True)

    framework = dest / 'framework-negative.dll'
    framework.write_bytes(build_pe(rdata_strings=['CMFCVisualManager']))
    assert TARGET not in scan(framework), 'framework surface must be excluded'
    print('PASS framework-negative.dll', flush=True)


if __name__ == '__main__':
    main()
