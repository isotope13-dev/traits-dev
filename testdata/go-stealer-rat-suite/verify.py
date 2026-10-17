"""Go stealer suite and SOCKS tasking composites.

Run: python3 testdata/go-stealer-rat-suite/verify.py <scratch-directory>

Go stealers (e.g. Salat) expose their toolkit as plaintext routine
names: `main.Steal`, `main.sendScreen`, `main.runKeylogger`, a
Chromium master-key routine, a `main.p2pSocks` proxy, and a `main.tloop`
task loop. UPX packing hides their strings but not these symbols, so
`go-keylogger-screen-browser-stealer-suite` (collection) and
`go-socks-proxied-task-loop` (tasking) convict on symbol quartets where
string-based composites miss.

Controls: minimal PE32 fixtures (padded past the 3MB symbol size gate)
carry the marker strings in .text. Each positive carries one full
quartet and must report only its own hostile; each negative drops one
leg and must report neither.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE = ('objectives/collection/multi-source::'
         'go-keylogger-screen-browser-stealer-suite')
TASKING = ('objectives/command-and-control/remote-command/tasking::'
           'go-socks-proxied-task-loop')

SUITE_FULL = ('main.runKeylogger', 'main.Steal', 'main.sendScreen',
              'chromium_master_key')
SUITE_DROP = ('main.runKeylogger', 'main.Steal', 'main.sendScreen')
SOCKS_FULL = ('main.p2pSocks', 'SOCKS5', 'main.tloop', 'c2Handler')
SOCKS_DROP = ('main.p2pSocks', 'SOCKS5', 'main.tloop')


def build_pe(markers):
    """Minimal PE32 over 3MB with marker strings inside .text."""
    text_blob = bytearray(b'\x33\xc0\xc3' + b'\x00' * 29)
    for s in markers:
        text_blob += s.encode('ascii') + b'\x00'
    while len(text_blob) % 4:
        text_blob += b'\x00'
    while len(text_blob) < 0x1000:
        text_blob += b'\x90' * 64
    text_blob = bytes(text_blob)

    size_headers = 0x200
    rva_text = 0x1000
    off_text = size_headers

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, 1, 0, 0, 0, 224, 0x0102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, rva_text, rva_text, rva_text)
    struct.pack_into('<III', opt, 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0x5000, size_headers, 0)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    pe += bytes(opt)
    pe += b'.text\x00\x00\x00'
    pe += struct.pack('<IIIIIIHHI', len(text_blob), rva_text, 0x1000,
                      off_text, 0, 0, 0, 0, 0x60000020)
    pe += b'\x00' * (size_headers - len(pe))
    pe += text_blob + b'\x00' * (0x1000 - len(text_blob))
    while len(pe) < 0x310000:
        pe += b'\x00' * 0x10000
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

    cases = [
        ('suite-positive.exe', SUITE_FULL, SUITE, TASKING),
        ('suite-negative.exe', SUITE_DROP, None, None),
        ('socks-positive.exe', SOCKS_FULL, TASKING, SUITE),
        ('socks-negative.exe', SOCKS_DROP, None, None),
    ]
    for name, markers, want, want_absent in cases:
        path = dest / name
        path.write_bytes(build_pe(markers))
        ids = scan(path)
        if want is None:
            assert SUITE not in ids and TASKING not in ids, \
                '%s must not convict' % name
        else:
            assert want in ids, '%s must convict' % name
            assert want_absent not in ids, '%s must not cross-fire' % name
        print('PASS %s' % name, flush=True)


if __name__ == '__main__':
    main()
