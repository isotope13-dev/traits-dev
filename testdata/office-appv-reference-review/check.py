"""Focused controls for executable references and native opcode interpretation."""
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'micro-behaviors/fs/path/basename::'
IMUL = 'metadata/binary/instruction/operand::x86-imul-31'


def pe(payload, il_only=False):
    image = bytearray(1024)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', image, opt, 0x10b)
    struct.pack_into('<I', image, opt + 4, 512)
    struct.pack_into('<IIIIII', image, opt + 16, 0x1000, 0x1000, 0, 0x400000, 0x1000, 512)
    struct.pack_into('<II', image, opt + 56, 0x2000, 512)
    struct.pack_into('<H', image, opt + 68, 3)
    struct.pack_into('<I', image, opt + 92, 16)
    sec = opt + 224
    image[sec:sec + 8] = b'.text\0\0\0'
    struct.pack_into('<IIII', image, sec + 8, 512, 0x1000, 512, 512)
    struct.pack_into('<I', image, sec + 36, 0x60000020)
    image[512:512 + len(payload)] = payload
    if il_only:
        struct.pack_into('<II', image, opt + 96 + 14 * 8, 0x1080, 72)
        struct.pack_into('<IHHIIII', image, 0x280, 72, 2, 5, 0x1100, 32, 1, 0x06000001)
        image[0x300:0x304] = b'BSJB'
        struct.pack_into('<HHII', image, 0x304, 1, 1, 0, 12)
        image[0x310:0x31c] = b'v4.0.30319\0\0'
    return image


def ids(path):
    result = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(path)],
        check=True, capture_output=True, text=True,
    )
    return {t['id']: t['crit'] for f in json.loads(result.stdout)['files']
            for t in f.get('traits', [])}


CASES = [
    ('two-names', b'\xc3\0icons.exe\0mavinject32.exe\0', False,
     ['office-icons-executable-reference', 'mavinject32-executable-reference',
      'mavinject32-name-reference', 'office-appv-executable-name-set'], []),
    ('single-name', b'\xc3\0icons.exe\0', False,
     ['office-icons-executable-reference'], ['office-appv-executable-name-set']),
    ('other-pair', b'\xc3\0icons.exe\0vpreview.exe\0', False,
     ['office-icons-executable-reference', 'office-vpreview-executable-reference',
      'office-appv-executable-name-set'], []),
    ('near-miss', b'\xc3\0icons.exe.txt\0vpreview.exe.txt\0', False,
     [], ['office-icons-executable-reference', 'office-vpreview-executable-reference',
          'office-appv-executable-name-set']),
    ('native-imul', b'\x6b\xc0\x1f\xc3', False, [], []),
    ('managed-data-imul', b'\x6b\xc0\x1f\xc3', True, [], []),
]

with tempfile.TemporaryDirectory() as directory:
    for name, payload, managed, positive, negative in CASES:
        path = Path(directory) / (name + '.exe')
        path.write_bytes(pe(payload, managed))
        observed = ids(path)
        for trait in positive:
            assert observed.get(PREFIX + trait) == 3, (name, trait, observed)
        for trait in negative:
            assert PREFIX + trait not in observed, (name, trait)
        assert not any('office-decoy' in trait for trait in observed), (name, observed)
        if name == 'native-imul':
            assert IMUL in observed, (name, observed)
        if name == 'managed-data-imul':
            assert IMUL not in observed, (name, observed)
        print(name + ': PASS')
