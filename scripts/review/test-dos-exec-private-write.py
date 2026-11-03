#!/usr/bin/env python3
"""Check DOS private-interrupt entry-write detection boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/infect/binary/dos/interrupt::dos-exec-private-body-entry-writer'
monitor = 'objectives/impact/degrade/edr/teardown::dos-entry-writer-uninstalls-virus-monitor'
scanner_delete = 'objectives/impact/degrade/edr/teardown::dos-entry-writer-scanner-name-delete'
parts = {
    'ivt': bytes.fromhex('C7 06 84 00 16 03 8C 06 86 00'),
    'exec': bytes.fromhex('80 FC 4B 74 01'),
    'read': bytes.fromhex('B4 3F B9 03 00 BA 46 05 CD 01'),
    'eof': bytes.fromhex('B8 02 42 33 C9 33 D2 CC'),
    'restore': bytes.fromhex('F3 A4 BB 00 01 FF E3'),
    'write': bytes.fromhex('B2 E9 88 16 56 05 90 90 B4 40 B9 52 04 BA 59 05 CD 01 B8 00 42 33 C9 33 D2 CD 01 B4 40 BA 56 05 B9 03 00 CC'),
}
def fixture(omit=None):
    return b'\x90'.join(value for name, value in parts.items() if name != omit) + b'\x90' * 256
av_request = bytes.fromhex('BA 45 59 B8 01 FA CD 16')
scanner_name = bytes.fromhex('26 81 7D FD 41 4E 75 18 26 81 7D FB 53 43 74')
delete = bytes.fromhex('B4 41 CC C3')
cases = {'complete.bin': (fixture(), True), 'complete-with-av.bin': (fixture() + av_request, True), 'av-only.bin': (av_request + b'\x90' * 256, False), 'complete-with-scanner-delete.bin': (fixture() + scanner_name + delete, True), 'no-scanner-name.bin': (fixture() + delete, True), 'no-delete.bin': (fixture() + scanner_name, True), 'scanner-delete-only.bin': (scanner_name + delete + b'\x90' * 256, False)}
for name in parts:
    cases['without-' + name + '.bin'] = (fixture(name), False)
changed = bytearray(fixture())
pos = changed.index(parts['write'])
changed[pos + 4] ^= 1
cases['relocated.bin'] = (bytes(changed), True)
changed = fixture().replace(bytes.fromhex('B9 03 00 CC'), bytes.fromhex('B9 04 00 CC'))
cases['different-entry-size.bin'] = (changed, False)
with tempfile.TemporaryDirectory(prefix='dos-private-review-') as tmp:
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
        monitor_found = monitor in {t['id'] for t in report.get('traits', [])}
        assert monitor_found == (name == 'complete-with-av.bin'), (name, monitor_found)
        scanner_found = scanner_delete in {t['id'] for t in report.get('traits', [])}
        assert scanner_found == (name == 'complete-with-scanner-delete.bin'), (name, scanner_found)
print('DOS private-interrupt entry-write boundaries passed.')
