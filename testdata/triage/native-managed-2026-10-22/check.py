#!/usr/bin/env python3
"""Static rule boundary controls. Never runs an analyzed executable.
Usage: python3 check.py <implant.exe> <scratch-output-directory>
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
LOGIN = 'objectives/credential-access/browser/chromium::rolling-xor-chromium-login-query'
COOKIE = 'objectives/credential-access/browser/chromium::rolling-xor-chromium-cookie-query'
XOR = 'objectives/anti-static/obfuscation/encoding/xor::native-xor-concealed-diagnostics'
CASCADE = 'objectives/evasion/process/injection/native::early-cascade-shim-injection'
REMOTE = 'objectives/evasion/process/injection/native::xor-concealed-remote-thread-injection'
queries = {
    LOGIN: b'SELECT origin_url, username_value, password_value FROM logins',
    COOKIE: b'SELECT host_key, name, path, is_secure, is_httponly, expires_utc, encrypted_value FROM cookies',
}

def scramble(value, key):
    out = bytearray()
    for i, byte in enumerate(value):
        out.append(byte ^ key)
        key = (key + i) & 127
    return bytes(out)

def inert_pe(data, section):
    """An entry-point RET and a separate, non-executed data section."""
    size = (len(data) + 511) // 512 * 512
    buf = bytearray(1024 + size)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    struct.pack_into('<H', buf, 0x98, 0x20b)
    struct.pack_into('<I', buf, 0x98 + 16, 0x1000)
    struct.pack_into('<Q', buf, 0x98 + 24, 0x140000000)
    struct.pack_into('<II', buf, 0x98 + 32, 0x1000, 512)
    struct.pack_into('<II', buf, 0x98 + 56, 0x3000 + size, 512)
    struct.pack_into('<H', buf, 0x98 + 68, 3)
    struct.pack_into('<I', buf, 0x98 + 108, 16)
    for off, name, va, raw, length in [(0x188, b'.entry', 0x1000, 512, 512),
                                      (0x1b0, section.encode(), 0x2000, 1024, size)]:
        buf[off:off + 8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', buf, off + 8, length, va, length, raw)
        struct.pack_into('<I', buf, off + 36, 0x60000020 if off == 0x188 else 0x40000040)
    buf[512] = 0xc3
    buf[1024:1024 + len(data)] = data
    return bytes(buf)

cases = []
def case(name, data, yes=(), no=()):
    path = OUT / (name + '.exe')
    path.write_bytes(data)
    cases.append((path, set(yes), set(no)))

# Separate controls exercise mask boundaries and the initial high bit.
for id, q in queries.items():
    name = 'logins' if id == LOGIN else 'cookies'
    for key in [0, 127, 128, 255]:
        case(name + '-key-' + str(key), inert_pe(scramble(q, key), '.rdata'), [id])
    case(name + '-plaintext', inert_pe(q, '.rdata'), no=[id])
    case(name + '-wrong-section', inert_pe(scramble(q, 42), '.data'), no=[id])
    benign = q.replace(b'password_value', b'display_name').replace(b'encrypted_value', b'display_name')
    case(name + '-different-fields', inert_pe(scramble(benign, 42), '.rdata'), no=[id])

loop = bytes.fromhex('44 0F B6 04 11 41 30 C0 44 88 04 13 48 FF C2 48 39 D6 75 EC')
for key in [1, 19, 255]:
    encoded = bytes(x ^ key for x in b'Could not ')
    case('xor-' + str(key), inert_pe(loop + b'\0' + encoded, '.text'), [XOR], [CASCADE, REMOTE])
case('plain-diagnostics', inert_pe(loop + b'Could not ', '.text'), no=[XOR])
case('xor-data-no-decoder', inert_pe(bytes(x ^ 19 for x in b'Could not '), '.text'), no=[XOR])

# Dependency removals from the actual implant exercise the full imported-API
# relation. The untouched original was independently reverse-engineered.
original = Path(sys.argv[1]).read_bytes()
case('implant-original', original, [CASCADE, XOR, REMOTE])
assert original.count(b'WriteProcessMemory\0') == 1
case('implant-without-remote-write', original.replace(b'WriteProcessMemory\0', b'XriteProcessMemory\0'),
     [XOR], [CASCADE, REMOTE])
pattern = bytes.fromhex('48 8B 3D D0 C3 12 00 83 E0 3F 44 2B E0 8B C2 41 8A CC')
assert original.count(pattern) == 1
case('implant-without-shim-pattern', original.replace(pattern, b'\0' * len(pattern)), [XOR, REMOTE], [CASCADE])
assert original.count(loop) == 1
case('implant-without-xor-loop', original.replace(loop, b'\x90' * len(loop)), [CASCADE], [XOR, REMOTE])

cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl']
result = subprocess.run(cmd + [str(p) for p, _, _ in cases], capture_output=True, text=True,
                        env={**os.environ, 'CLEAVE_VALIDATE': '0'}, check=True)
(OUT / 'reports.jsonl').write_text(result.stdout)
(OUT / 'scan.log').write_text(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    for f in json.loads(line).get('files', []):
        reports[str(Path(f['path']).resolve())] = {t['id'] for t in f.get('traits', [])}
record = []
for path, yes, no in cases:
    actual = reports[str(path.resolve())]
    assert yes <= actual and not (no & actual), (path.name, yes - actual, no & actual)
    record.append({'case': path.name, 'matched': sorted(yes), 'not_matched': sorted(no)})
(OUT / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
print(f'PASS: {len(cases)} static boundary controls')
