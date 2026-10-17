"""Hook spy with a download channel instead of Winsock.

Run: python3 testdata/hook-spy-download-channel/verify.py <scratch-directory>

`hook-debugpriv-process-control-network-channel` convicts an unsigned binary
combining a full window-hook lifecycle, SeDebugPrivilege-gated process
access, process termination, thread creation, and a network channel. The
channel leg used to require the WSOCK32 marker, so hook-based spyware that
reaches the network through a URLMon download (URLDownloadToFile) missed
conviction. The leg now accepts either channel.

Controls: the URLMon positive and the WSOCK32 positive must both report the
hostile; removing the hook pair or removing every network leg must not.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/collection/multi-source::'
          'hook-debugpriv-process-control-network-channel')

BASE_IMPORTS = [
    ('USER32.dll', 'SetWindowsHookExW'),
    ('USER32.dll', 'CallNextHookEx'),
    ('ADVAPI32.dll', 'OpenProcessToken'),
    ('ADVAPI32.dll', 'AdjustTokenPrivileges'),
    ('KERNEL32.dll', 'OpenProcess'),
    ('KERNEL32.dll', 'TerminateProcess'),
    ('KERNEL32.dll', 'CreateThread'),
]


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(imports, rdata_strings=()):
    """Minimal PE32 with the given import table and rdata strings."""
    text_blob = b'\x33\xc0\xc3' + b'\x00' * 29
    while len(text_blob) % 4:
        text_blob += b'\x00'

    size_headers, file_align, sec_align = 0x200, 0x200, 0x1000
    rva_text, rva_rdata = 0x1000, 0x2000
    off_text, off_rdata = size_headers, size_headers + 0x200

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

    rdata = bytearray(0x200)
    for s in strblobs:
        rdata[str_off:str_off + len(s)] = s
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
    hookless = [i for i in BASE_IMPORTS
                if i[1] not in ('SetWindowsHookExW', 'CallNextHookEx')]
    cases = {
        # New coverage: hook spy reaching the net through URLMon download.
        'hook-urlmon-positive.exe': (
            build_pe(BASE_IMPORTS + [('URLMON.dll', 'URLDownloadToFileW')],
                     ['SeDebugPrivilege']), True),
        # Pre-existing coverage: the Winsock channel variant still convicts.
        'hook-wsock32-positive.exe': (
            build_pe(BASE_IMPORTS + [('WSOCK32.dll', 'send')],
                     ['SeDebugPrivilege']), True),
        # Same spy surface without the hook pair: no conviction.
        'hookless-negative.exe': (
            build_pe(hookless + [('URLMON.dll', 'URLDownloadToFileW')],
                     ['SeDebugPrivilege']), False),
        # Same spy surface without any network leg: no conviction.
        'nonet-negative.exe': (
            build_pe(BASE_IMPORTS, ['SeDebugPrivilege']), False),
    }
    for name, (blob, hostile) in cases.items():
        path = dest / name
        path.write_bytes(blob)
        assert (TARGET in scan(path)) == hostile, name
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
