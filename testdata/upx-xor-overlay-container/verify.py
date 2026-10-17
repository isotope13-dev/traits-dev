"""UPX/XOR/overlay container threshold covers mid-size overlays.

Run: python3 testdata/upx-xor-overlay-container/verify.py <scratch-directory>

`xor-decoder-in-upx-overlay-pe-carrier` convicts a UPX image combining
an unrolled XOR decoder with an embedded-PE overlay. The size leg used
to demand half the image, which missed verified carriers staging a
60KB-plus overlay PE beside the decoder at ~42% of the file; it now
requires thirty-five percent. The other four legs (UPX section pair,
embedded DOS header, XOR decoder bytes, VirtualProtect) carry the
specificity either way.

Controls: a minimal PE32 with UPX0/UPX1 sections, the decoder pattern,
a VirtualProtect import, an embedded DOS header in the overlay, and a
40% overlay must report the hostile; the same image with a 10% overlay
must not.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTAINER = ('objectives/anti-static/obfuscation/payload/container::'
             'xor-decoder-in-upx-overlay-pe-carrier')

XOR_DECODER = bytes([
    0x0F, 0xB6, 0x50, 0x01, 0x80, 0xF1, 0x02, 0x80, 0xF2, 0x03,
    0x88, 0x4C, 0x24, 0x04, 0x0F, 0xB6, 0x48, 0x05, 0x88, 0x54,
    0x24, 0x06, 0x0F, 0xB6, 0x50, 0x07, 0x80, 0xF1, 0x08, 0x80,
    0xF2, 0x09, 0x88, 0x4C, 0x24, 0x0A,
])
DOS_HEADER = bytes.fromhex('4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00')


def build_pe(overlay_ratio):
    """Minimal PE32 with UPX sections, decoder bytes, and a sized overlay."""
    text_blob = b'\x33\xc0\xc3' + XOR_DECODER + b'\x90' * 64
    upx0 = b'\x00' * 0x200
    # Sized so section data ends past 4096: the embedded-header atom only
    # matches at file offset 4096 and above.
    upx1 = b'\x90' * 0x800

    rdata = bytearray(0x200)
    rva_rdata = 0x4000
    ilt_off, ilt_size = 40, 8
    dllname = b'KERNEL32.dll'
    doff = ilt_off + ilt_size + 18
    struct.pack_into('<IIIII', rdata, 0, 0, 0, 0,
                     rva_rdata + doff, rva_rdata + ilt_off)
    struct.pack_into('<I', rdata, ilt_off, rva_rdata + ilt_off + ilt_size)
    o = ilt_off + ilt_size
    rdata[o:o + 2] = b'\x00\x00'
    rdata[o + 2:o + 2 + len('VirtualProtect')] = b'VirtualProtect'
    rdata[doff:doff + len(dllname)] = dllname

    secs = [('UPX0', 0x1000, upx0, 0xE0000020),
            ('UPX1', 0x2000, upx1, 0xE0000020),
            ('.text', 0x3000, text_blob, 0x60000020),
            ('.rdata', rva_rdata, bytes(rdata), 0x40000040)]
    size_headers = 0x400
    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, len(secs), 0, 0, 0, 224, 0x0102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<III', opt, 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0x6000, size_headers, 0)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    struct.pack_into('<II', opt, 104, rva_rdata, 0x200)
    pe += bytes(opt)
    off = size_headers
    blobs = []
    for nm, vr, blob, ch in secs:
        raw = (len(blob) + 0x1FF) // 0x200 * 0x200
        pe += nm.encode('ascii').ljust(8, b'\x00')
        pe += struct.pack('<IIIIIIHHI', len(blob), vr, raw, off,
                          0, 0, 0, 0, ch)
        off += raw
        blobs.append(blob + b'\x00' * (raw - len(blob)))
    pe += b'\x00' * (size_headers - len(pe))
    for blob in blobs:
        pe += blob
    base_len = len(pe)
    overlay_len = int(base_len * overlay_ratio / (1 - overlay_ratio))
    overlay = bytearray(overlay_len)
    overlay[0:len(DOS_HEADER)] = DOS_HEADER
    pe += bytes(overlay)
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

    positive = dest / 'xor-overlay-40pct.exe'
    positive.write_bytes(build_pe(0.40))
    ids = scan(positive)
    assert CONTAINER in ids, '40% overlay container must convict'
    print('PASS xor-overlay-40pct.exe', flush=True)

    negative = dest / 'xor-overlay-10pct.exe'
    negative.write_bytes(build_pe(0.10))
    ids = scan(negative)
    assert CONTAINER not in ids, '10% overlay must not convict'
    print('PASS xor-overlay-10pct.exe', flush=True)


if __name__ == '__main__':
    main()
