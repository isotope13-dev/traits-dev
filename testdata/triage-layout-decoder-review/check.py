"""Inert PE controls for the layout/decoder review; no sample bytes included.

The entry point returns. Decoder signatures in .data are never executed.
Large random data is a benign counterexample to the old encryption inference.
"""
from pathlib import Path
import random
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
DECODER = 'micro-behaviors/data/decode/xor::x86-signed-cyclic-key-xor-data'
DATA = 'metadata/binary/section/ratio::dominant-high-entropy-data'
LOWER = 'metadata/binary/section/label::long-lowercase-section-name'
LABELS = 'metadata/binary/section/label::high-entropy-nonstandard-section-names'
RUN = 'micro-behaviors/os/registry/keys/autostart::run-or-runonce-key-reference'


def pe(sections):
    align = lambda n, a: (n + a - 1) // a * a
    hdr = align(0x178 + 40 * len(sections), 0x200)
    raw, rva = hdr, 0x1000
    table = []
    for name, data, flags in sections:
        size = align(len(data), 0x200)
        table.append((name, data, flags, raw, rva, size))
        raw += size
        rva += align(size, 0x1000)
    b = bytearray(raw)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, len(table), 0, 0, 0, 224, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<I', b, o + 16, 0x1000)
    struct.pack_into('<I', b, o + 28, 0x400000)
    struct.pack_into('<II', b, o + 32, 0x1000, 0x200)
    struct.pack_into('<II', b, o + 56, rva, hdr)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 92, 16)
    for i, (name, data, flags, raw, rva, size) in enumerate(table):
        q = 0x178 + 40 * i
        b[q:q + len(name)] = name.encode()
        struct.pack_into('<IIII', b, q + 8, len(data), rva, size, raw)
        struct.pack_into('<I', b, q + 36, flags)
        b[raw:raw + len(data)] = data
    return b


def image(data, name='.data'):
    return pe([('.text', b'\xc3', 0x60000020), (name, data, 0xc0000040)])


code = bytes.fromhex('0f be 04 38 99 f7 fb 8b c6 80 c2 4f 30 11 59 99 f7 f9 47 85 d2 75 02 33 ff 46')
rng = random.Random(31847)
random_data = bytes(rng.getrandbits(8) for _ in range(262144))
msvc_names = ['.text', '.rdata', '.data', '.pdata', '.00cfg', '.gehcont', '.retplne', '.tls', 'CPADinfo', '_RDATA', '.rsrc', '.reloc']
cases = [
    ('decoder', image(code), {DECODER: True}),
    ('different-key-addend', image(code.replace(b'\x80\xc2\x4f', b'\x80\xc2\x23')), {DECODER: True}),
    ('store-without-xor', image(code.replace(b'\x30\x11', b'\x88\x11')), {DECODER: False}),
    ('large-random-data', image(random_data), {DATA: True}),
    ('large-zero-data', image(bytes(262144)), {DATA: False}),
    ('long-lowercase', image(b'\0' * 512, '.abcdefg'), {LOWER: True}),
    ('label-with-digit', image(b'\0' * 512, '.abcdef1'), {LOWER: False}),
    ('msvc-mitigations', pe([(n, b'\xc3' + bytes(511), 0x60000020 if n == '.text' else 0x40000040) for n in msvc_names]), {LOWER: True, LABELS: True}),
    ('run-key-reference-only', image(b'Software\\Microsoft\\Windows\\CurrentVersion\\Run\0' + bytes(60000)), {RUN: True}),
    ('unrelated-registry-reference', image(b'Software\\Vendor\\Preferences\0' + bytes(60000)), {RUN: False}),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, data, expected in cases:
        p = Path(tmp) / (name + '.exe')
        p.write_bytes(data)
        result = subprocess.run(['cleave', '--traits-dir', str(ROOT), 'test-rules', str(p), '--rules', ','.join(expected)], text=True, capture_output=True, check=True)
        for trait, wanted in expected.items():
            actual = any(line.startswith('MATCHED ' + trait + ' ') for line in result.stdout.splitlines())
            assert actual == wanted, (name, trait, wanted, result.stdout, result.stderr)
        print('PASS', name)
