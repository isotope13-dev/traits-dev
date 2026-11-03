#!/usr/bin/env python3
"""Check the resident DOS executable rewrite pattern and its boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/infect/binary/dos/interrupt::dos-vector-sft-mz-header-rewrite'
parts = {
    'get-vector': bytes.fromhex('B8 21 35 CD 21'),
    'set-vector': bytes.fromhex('B8 21 24 FE C4 CD 21'),
    'header': bytes.fromhex('B9 18 00 BA BA 03 B4 3F CD 21 3B C8 75 10 8B 0E BA 03 81 F9 5A 4D'),
    'write': bytes.fromhex('BA 00 01 B9 B6 02 B4 40 50 CD 21 E8 2E FF B9 00 02 F7 F1 85 D2 74 01 40 A3 BE 03 89 16 BC 03 99 26 89 55 15 26 89 55 17 BA BA 03 B9 18 00 58 CD 21'),
    'time': bytes.fromhex('B8 01 57 CD 21'),
}

def fixture(omit=None):
    return b'\x90'.join(v for k, v in parts.items() if k != omit) + b'\x90' * 256

cases = {'complete.bin': (fixture(), True)}
for name in parts:
    cases['without-' + name + '.bin'] = (fixture(name), False)
cases['relocated.bin'] = (fixture().replace(bytes.fromhex('BA BA 03'), bytes.fromhex('BA 34 12')), True)
cases['short-header.bin'] = (fixture().replace(bytes.fromhex('B9 18 00'), bytes.fromhex('B9 17 00')), False)
cases['no-cursor-reset.bin'] = (fixture().replace(bytes.fromhex('26 89 55 17'), bytes.fromhex('90 90 90 90')), False)
with tempfile.TemporaryDirectory(prefix='dos-sft-mz-') as tmp:
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
print('DOS SFT executable rewrite pattern boundaries passed.')
