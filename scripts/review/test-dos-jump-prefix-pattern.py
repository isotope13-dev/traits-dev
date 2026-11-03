#!/usr/bin/env python3
"""Check ordered DOS jump-prefix code and loose-cooccurrence boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/infect/binary/dos/file::dos-search-and-jump-prefix-write'
parts = {
    'find-first': bytes.fromhex('B4 4E CD 21'),
    'find-next': bytes.fromhex('B4 4F CD 21'),
    'seek-end': bytes.fromhex('B8 02 42 CD 21'),
    'time': bytes.fromhex('B8 01 57 CD 21'),
    'patch': bytes.fromhex('8D B6 EC 04 8D BE C7 04 56 B9 03 00 F3 A4 5F B0 E9 AA 58 2D 03 00 AB 33 C9 8D 96 0D 05 B8 01 43 CD 21 B4 3D B0 02 CD 21 93 B4 40 B9 03 00 8D 96 EC 04 CD 21'),
}
def fixture(omit=None):
    return b'\x90'.join(v for k, v in parts.items() if k != omit) + b'\x90' * 256
cases = {'complete.bin': (fixture(), True)}
for name in parts:
    cases['without-' + name + '.bin'] = (fixture(name), False)
cases['alternate-open.bin'] = (fixture().replace(bytes.fromhex('B4 3D B0 02'), bytes.fromhex('B8 02 3D')), True)
cases['loose-calls.bin'] = (b'\x90'.join(v for k,v in parts.items() if k != 'patch') + bytes.fromhex('B0 E9 AA B4 40 CD 21') + b'\x90' * 256, False)
changed = bytearray(fixture())
pos = changed.index(parts['patch'])
changed[pos + 2] ^= 1
cases['relocated.bin'] = (bytes(changed), True)
with tempfile.TemporaryDirectory(prefix='dos-jump-prefix-') as tmp:
    paths = []
    for name, (data, _) in cases.items():
        path = Path(tmp) / name
        path.write_bytes(data)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).name
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, cases[name][1])
print('DOS jump-prefix pattern boundaries passed.')
