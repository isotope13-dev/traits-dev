"""PicoScope suite context suppresses protector/imaging conclusions.

Run: python3 testdata/picoscope-suite-context/verify.py <scratch-directory>

PicoScope ships obfuscated assemblies whose protector checks .NET
profiler variables, while its interop layer pairs OpenCV imaging pixel
reads with IoC plugin dispatch. `dotnet-profiler-anti-debug` and the
bitmap-stego composites therefore fire on vendor protection and
oscilloscope imaging, not hostile behavior; `picoscope-suite-context`
(PicoScope7 build-farm path fragment) suppresses them.

Controls: the profiler-check positive and the pixel-channel positive (no
Pico markers) must report their hostile/suspicious; the same images with
the PicoScope7 marker must report neither.
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
RED_CHANNEL = ('objectives/anti-static/obfuscation/steganography/image::'
               'dotnet-red-channel-byte-collection')
DECOMPOSITION = ('objectives/anti-static/obfuscation/steganography/image::'
                 'dotnet-pixel-channel-decomposition')

PROFILER_IMPORTS = [
    ('KERNEL32.dll', 'GetProcAddress'),
]
DOTNET_IMPORTS = [
    ('mscoree.dll', '_CorExeMain'),
]

PROFILER_STRINGS = (
    'COR_ENABLE_PROFILING',
    'GetEnvironmentVariable',
)
# BSJB (metadata root) + pixel channel words + GetObject, all observable
# from .text so section-scoped atoms match a minimal fixture.
STEGO_STRINGS = (
    'BSJB',
    'GetPixel',
    'get_R\x00',
    'get_G\x00',
    'get_B\x00',
    'GetObject',
)
PICO_MARKER = 'C:\\a\\1\\s\\PicoScope7\\Pico.Interop.Common.pdb'


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

    negative = dest / 'profiler-pico-negative.exe'
    negative.write_bytes(
        build_pe(PROFILER_IMPORTS, PROFILER_STRINGS + (PICO_MARKER,)))
    ids = scan(negative)
    assert PROFILER not in ids, 'PicoScope context must suppress anti-debug'
    print('PASS profiler-pico-negative.exe', flush=True)

    stego = dest / 'pixel-channel-positive.exe'
    stego.write_bytes(build_pe(DOTNET_IMPORTS, STEGO_STRINGS))
    ids = scan(stego)
    assert RED_CHANNEL in ids, 'pixel channel pattern must report'
    assert DECOMPOSITION in ids, 'channel decomposition must report'
    print('PASS pixel-channel-positive.exe', flush=True)

    stego_neg = dest / 'pixel-channel-pico-negative.exe'
    stego_neg.write_bytes(
        build_pe(DOTNET_IMPORTS, STEGO_STRINGS + (PICO_MARKER,)))
    ids = scan(stego_neg)
    assert RED_CHANNEL not in ids, 'PicoScope context must suppress stego'
    assert DECOMPOSITION not in ids, 'PicoScope context must suppress stego'
    print('PASS pixel-channel-pico-negative.exe', flush=True)


if __name__ == '__main__':
    main()
