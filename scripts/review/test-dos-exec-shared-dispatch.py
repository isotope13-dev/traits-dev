#!/usr/bin/env python3
"""Check DOS resident EXEC and shared-dispatch detection boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/infect/binary/dos/interrupt::dos-resident-exec-four-byte-appender'
parts = {
    'vector': bytes.fromhex('33 C0 8E D8 BE 84 00 BF DE 00 B1 02 F3 A5 E8 DA 00 FA C7 44 FC 84 00 8C 44 FE FB'),
    'exec': bytes.fromhex('80 FC 4B 74 08'),
    'open': bytes.fromhex('B8 92 3D CD 21'),
    'read': bytes.fromhex('B4 3F B1 04 0E 1F BA 2F 01 CD 21 80 3E 2F 01 4D 74'),
    'calls': bytes.fromhex('B0 02 E8 2B 00 A3 02 00 B9 99 01 E8 1C 00 E8 1D 00 B1 04 E8 14 00 E8 49 00 B4 3E CD 21'),
    'dispatch': bytes.fromhex('B4 40 EB 06 32 C0 33 C9 B4 42 33 D2 CD 21 C3'),
    'time': bytes.fromhex('B8 01 57 CD 21'),
}
def fixture(omit=None):
    return b'\x90'.join(value for name, value in parts.items() if name != omit) + b'\x90' * 256
cases = {'complete.bin': (fixture(), True)}
for name in parts:
    cases['without-' + name + '.bin'] = (fixture(name), False)
changed = bytearray(fixture())
pos = changed.index(parts['vector'])
changed[pos + 8] ^= 1  # relocated copy destination, a wildcard operand
cases['relocated.bin'] = (bytes(changed), True)
with tempfile.TemporaryDirectory(prefix='dos-shared-review-') as tmp:
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
print('DOS EXEC/shared-dispatch boundaries passed.')
