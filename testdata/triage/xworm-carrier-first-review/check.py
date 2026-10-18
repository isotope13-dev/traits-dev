"""Check contained-family identity independently of executable behavior."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TRAIT = 'well-known/malware/rat/xworm::xworm-embedded-client'
DOS = bytes.fromhex('4d5a90000300000004000000ffff0000')
COMMANDS = ['Urlhide', 'PCShutdown', 'RunShell', 'OfflineGet', 'injRun', 'UACFunc']


def pe(payload, section=b'.rdata'):
    raw_size = (len(payload) + 511) & ~511
    data = bytearray(512 + raw_size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x8664, 1, 0, 0, 0, 240, 0x22)
    struct.pack_into('<H', data, 152, 0x20b)
    struct.pack_into('<Q', data, 152 + 24, 0x140000000)
    for off, value in [(16, 4096), (32, 4096), (36, 512),
                       (56, 8192), (60, 512), (108, 16)]:
        struct.pack_into('<I', data, 152 + off, value)
    struct.pack_into('<H', data, 152 + 68, 2)
    struct.pack_into('<8sIIIIIIHHI', data, 392, section,
                     len(payload), 4096, raw_size, 512, 0, 0, 0, 0, 0x40000040)
    data[512:512 + len(payload)] = payload
    return bytes(data)


def content(commands, dos=DOS, clr=b'BSJB'):
    return dos + b'\0' * 32 + clr + b'\0' * 16 + b''.join(
        token.encode('utf-16le') + b'\0\0' for token in commands)


with tempfile.TemporaryDirectory(prefix='xworm-carrier-') as tmp:
    # Keep generated controls within the caller-selected scratch directory.
    cases = [
        ('six-commands', pe(content(COMMANDS)), True),
        ('four-commands', pe(content(COMMANDS[:4])), True),
        ('renamed-container', pe(content(COMMANDS)), True),
        ('three-commands', pe(content(COMMANDS[:3])), False),
        ('no-clr', pe(content(COMMANDS, clr=b'----')), False),
        ('no-dos', pe(content(COMMANDS, dos=b'-' * len(DOS))), False),
        ('wrong-section', pe(content(COMMANDS), section=b'.data'), False),
        ('generic-http', pe(DOS + b'BSJB\0POST / HTTP/1.1\0'), False),
    ]
    paths = []
    for name, data, _ in cases:
        path = Path(tmp) / (name + '.exe')
        path.write_bytes(data)
        paths.append(path)
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', *(str(path) for path in paths),
    ], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        observed.update((f['path'], {t['id'] for t in f.get('traits', [])})
                        for f in report['files'])
        remaining = remaining[end:].lstrip()
    for path, (name, _, expected) in zip(paths, cases):
        assert (TRAIT in observed[str(path)]) == expected, name
    print(f'{len(cases)} embedded-client controls passed')
