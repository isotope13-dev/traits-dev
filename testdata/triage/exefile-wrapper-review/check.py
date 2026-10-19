"""Control RIP-relative target binding without executing the specimen."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
WRITE = 'micro-behaviors/os/registry/write::native-exefile-wrapper-registration'
KEY = 'micro-behaviors/os/registry/keys/execution::exefile-open-command-key'
XOR = 'micro-behaviors/os/registry/keys/execution::xor-exefile-open-command-key'
VALUE = 'micro-behaviors/os/registry/value-name::isolatedcommand-value-name'
original = Path(sys.argv[1]).read_bytes()
path = b'exefile\\shell\\open\\command'


def patched(offset, replacement):
    data = bytearray(original)
    data[offset:offset + len(replacement)] = replacement
    return data


key_load = original.index(bytes.fromhex('48 8d 15 ec c5 04 00 48 c7 c1'))
value_load = original.index(bytes.fromhex('48 8d 15 ad c5 04 00 48 8b 1d'))
append = original.index(bytes.fromhex('48 b9 20 22 25 31 22 20 25 2a'))
path_offset = original.index(path)
cases = [
    ('original', original, {WRITE, KEY, VALUE}, {XOR}),
    ('renamed', original, {WRITE, KEY, VALUE}, {XOR}),
    # All strings and imports remain: only the addressed value changes.
    ('wrong-key-target', patched(key_load + 3, b'\xed'), {KEY, VALUE}, {WRITE}),
    ('wrong-value-target', patched(value_load + 3, b'\xae'), {KEY, VALUE}, {WRITE}),
    ('wrong-hive', patched(key_load + 10, b'\x01'), {KEY, VALUE}, {WRITE}),
    ('no-forwarded-args', patched(append + 4, b'x'), {KEY, VALUE}, {WRITE}),
    ('no-value-write-api', original.replace(b'RegSetValueExA', b'RegGetValueExA'),
     {KEY, VALUE}, {WRITE}),
    ('different-association', patched(path_offset, b'txtfile'), {VALUE}, {WRITE, KEY}),
    ('xor-association', patched(path_offset, bytes(c ^ 0x37 for c in path)),
     {XOR, VALUE}, {WRITE, KEY}),
]

with tempfile.TemporaryDirectory(prefix='exefile-wrapper-') as tmp:
    paths = []
    for name, data, _, _ in cases:
        destination = Path(tmp) / (name + '.exe')
        destination.write_bytes(data)
        paths.append(destination)
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--disable', 'third-party', '--format', 'json',
        *(str(p) for p in paths),
    ], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        observed.update((f['path'], {t['id'] for t in f.get('traits', [])})
                        for f in report['files'])
        remaining = remaining[end:].lstrip()
    for p, (name, _, required, forbidden) in zip(paths, cases):
        found = observed[str(p)]
        assert required <= found, (name, 'missing', required - found)
        assert not forbidden & found, (name, 'unexpected', forbidden & found)
    print(f'{len(cases)} EXE-wrapper controls passed')
