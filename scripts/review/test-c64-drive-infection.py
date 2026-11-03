#!/usr/bin/env python3
"""Test C64 drive-infector coverage against missing and altered behaviors."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/infect/binary/c64::drive-resident-directory-infector'
header = bytes.fromhex('01 08 0B 08 C8 07 9E 32 30 35 39 00')
parts = {
    'upload': bytes.fromhex('A2 05 BD 9E 08 20 DD ED CA 10 F7'),
    'track': bytes.fromhex('A9 12 8D 00 04 85 08 85 0A 85 0C'),
    'job': bytes.fromhex('A9 90 2C A9 80 A2 03 95 00 B5 00 30 FC C9 01'),
    'redirect': bytes.fromhex('BD C6 05 91 C0 85 09 88 A9 12 91 C0'),
    'marker': bytes.fromhex('A9 00 85 0D 20 B4 04 A5 C3 8D A7 06 4C B1 04'),
}
def fixture(omit=None):
    return header + b'\xea' * 8 + b'\xea'.join(v for k, v in parts.items() if k != omit)
cases = {'positive': (fixture(), True), 'basic-only': (header + b'\xea' * 32, False)}
for key in parts:
    cases['without-' + key] = (fixture(key), False)
changed = bytearray(fixture())
changed[0] = 2
cases['wrong-load-address'] = (bytes(changed), False)
changed = bytearray(fixture())
changed[2] = 0
cases['wrong-basic-link'] = (bytes(changed), False)
# Relocating wildcard operands should not evade this behavioral combination.
changed = bytearray(fixture())
idx = changed.index(parts['upload'])
changed[idx + 3:idx + 5] = b'\x52\x09'
cases['relocated-upload'] = (bytes(changed), True)
with tempfile.TemporaryDirectory(prefix='c64-infection-review-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / name
        path.write_bytes(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split("\n") if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).name
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, report.get('type'))
print('C64 drive-infection boundaries passed.')
