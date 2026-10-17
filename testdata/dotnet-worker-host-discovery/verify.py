"""dotnet worker host discovery suppresses profiler anti-debug.

Run: python3 testdata/dotnet-worker-host-discovery/verify.py <scratch-directory>

Managed tools that bootstrap an isolated ``dotnet`` worker (test
runners, build tools, evolution workers such as AiDotNet.Evolution.Ptx)
read ``DOTNET_HOST_PATH``/``DOTNET_ROOT`` to locate the host and launch
the child process. Those host-discovery reads trip the profiling
environment leg of ``dotnet-profiler-anti-debug`` even though the
program never reacts to a profiler; the host-path atom suppresses the
composite while a genuine profiler check still convicts.

Controls: the profiler-check positive (profiling variable read plus
GoEnvironmentVariable-style resolver, no host discovery) must report the
hostile; the same image with the host-path marker must report neither
the hostile nor lose the notable host-discovery atom; the host-path
marker alone must not convict.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILER = ('objectives/anti-analysis/debugger-detect/combined-checks::'
            'dotnet-profiler-anti-debug')
HOST_PATH = ('micro-behaviors/os/env/platform::'
             'dotnet-host-path-env-name')

PROFILER_IMPORTS = [
    ('KERNEL32.dll', 'GetProcAddress'),
]

PROFILER_STRINGS = (
    'COR_ENABLE_PROFILING',
    'GetEnvironmentVariable',
)
WORKER_STRINGS = PROFILER_STRINGS + (
    'DOTNET_HOST_PATH',
    'DOTNET_ROOT',
    'FindDotnetHost',
)
HOST_ONLY_STRINGS = (
    'DOTNET_HOST_PATH',
    'GetEnvironmentVariable',
)


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(imports, text_strings=(), text_size=0x1400,
             rdata_strings=('mscorlib, Version=4.0.0.0',)):
    """Minimal PE32 over 4KB with marker strings inside .text."""
    text_blob = bytearray(b'\x33\xc0\xc3' + b'\x00' * 29)
    for s in text_strings:
        text_blob += s.encode('ascii') + b'\x00'
    while len(text_blob) % 4:
        text_blob += b'\x00'
    while len(text_blob) < text_size:
        text_blob += b'\x90' * 64
    text_blob = bytes(text_blob)

    size_headers, file_align, sec_align = 0x200, 0x200, 0x1000
    rva_text, rva_rdata = 0x1000, 0x2000
    off_text, off_rdata = size_headers, size_headers + align(
        len(text_blob), file_align)

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
    for dll, o in dllname_off.items():
        rdata[o:o + len(dll)] = dll.encode('ascii')

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
    pe += text_blob + b'\x00' * (align(len(text_blob), file_align)
                                 - len(text_blob))
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

    positive = dest / 'profiler-check-positive.exe'
    positive.write_bytes(build_pe(PROFILER_IMPORTS, PROFILER_STRINGS))
    ids = scan(positive)
    assert PROFILER in ids, 'profiler check must convict'
    print('PASS profiler-check-positive.exe', flush=True)

    negative = dest / 'profiler-worker-negative.exe'
    negative.write_bytes(build_pe(PROFILER_IMPORTS, WORKER_STRINGS))
    ids = scan(negative)
    assert PROFILER not in ids, 'worker host discovery must suppress it'
    assert HOST_PATH in ids, 'host-discovery atom must still report'
    print('PASS profiler-worker-negative.exe', flush=True)

    host_only = dest / 'host-discovery-only.exe'
    host_only.write_bytes(build_pe(PROFILER_IMPORTS, HOST_ONLY_STRINGS))
    ids = scan(host_only)
    assert PROFILER not in ids, 'host discovery alone must not convict'
    assert HOST_PATH in ids, 'host-discovery atom must report'
    print('PASS host-discovery-only.exe', flush=True)


if __name__ == '__main__':
    main()
