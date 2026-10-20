#!/usr/bin/env python3
"""Exercise decoded control flow, changing keys, and non-infection near misses."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
CODE = 'objectives/impact/infect/binary/dos/overwrite::dos-call-xor-dta-overwrite-code'
OVERWRITE = 'objectives/impact/infect/binary/dos/overwrite::dos-xor-loop-reencrypt-overwrite'
FAMILY = 'well-known/malware/virus/trivial::trivial-xor-encrypted-overwriter'
BASE = bytes.fromhex('b44eba1c01e81f00e119301ea5811fa71d22d23e8cf4143556504b5e35315c50521fab5fa51f1eb91f00be080180341f46e2fab138cd21c3')

def variant(key=31, patches=()):
    body = bytearray(BASE)
    for i in range(8, 39):
        body[i] ^= 31
    for offset, data in patches:
        body[offset:offset + len(data)] = data
    body[47] = key
    for i in range(8, 39):
        body[i] ^= key
    return bytes(body)

with tempfile.TemporaryDirectory(prefix='dos-xor-dta-') as tmp:
    cases = []
    for key in (1, 31, 32, 127, 254, 255):
        for ext in ('com', 'bin'):
            cases.append((f'key-{key}.{ext}', variant(key), True))
    # The unused family text can change without affecting behavior.
    cases.append(('renamed-marker.com', variant(37, [(23, b'HELLO')]), True))
    # Each removes one material part of the source-to-overwrite chain.
    for name, patches in (
        ('wrong-call-target', [(6, b'\x1e')]),
        ('read-only-open', [(16, b'\x00')]),
        ('not-dta-name', [(13, b'\x80')]),
        ('not-self-image', [(37, b'\x20')]),
        ('wrong-handle', [(20, b'\x90')]),
        ('unreachable-write', [(22, b'\x0c')]),
        ('wrong-key-pointer', [(10, b'\x30')]),
        ('decode-short-region', [(40, b'\x1e')]),
        ('partial-image-copy', [(52, b'\x30')]),
        ('non-executable-mask', [(30, b'TXT')]),
    ):
        cases.append((name + '.com', variant(patches=patches), False))
    # Retain neutral XOR/write setup, but remove the decoded file-opening path.
    cases.append(('xor-write-setup-only.com', variant(patches=[(12, b'\x90' * 11)]), False))
    # Preserve the previously recognized Trivial.82 encrypted layout.
    old_body = bytes.fromhex('b44eba4001cd21ba9e00b8023dcd21b74093ba0003b152cd21b8015733c9cd21')
    old = bytes.fromhex('be090180341f46e2fa') + bytes(c ^ 31 for c in old_body)
    cases.append(('prior-encrypted-layout.com', old, None))
    paths = []
    for name, data, _ in cases:
        path = Path(tmp) / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths],
                            text=True, capture_output=True, check=True)
    reports = {}
    for line in result.stdout.splitlines():
        for report in json.loads(line).get('files', []):
            reports[Path(report['path']).name] = report
    for name, _, expected in cases:
        traits = {t['id']: t for t in reports[name].get('traits', [])}
        if expected is None:
            assert FAMILY in traits, (name, traits)
        else:
            for trait in (CODE, OVERWRITE, FAMILY):
                assert (trait in traits) == expected, (name, trait, expected, traits)
            if expected:
                assert all(traits[t]['crit'] == 5 for t in (OVERWRITE, FAMILY))
    print(f'{len(cases)} controls passed: varying keys, renamed text, broken paths, prior layout')
