#!/usr/bin/env python3
"""Check cache-path, API and objective-admission bindings without executing PEs."""
import argparse
import json
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAPABILITY = 'micro-behaviors/process/deploy/file-exec::x86-urlmon-cache-path-winexec'
OBJECTIVE = 'objectives/execution/payload/file-exec::association-hijacker-cache-payload-launch'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('sample', type=Path)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
body = args.sample.read_bytes()
assert body[0x52b3:0x52b8] == bytes.fromhex('68 04 d4 40 00')

# A fragment containing only the two code blocks, their API-name constant,
# and the existing import tables. It retains the neutral cache-to-process
# mechanism and cannot meet the association-hijack objective. It is a static
# boundary control, not a claim that the full original program is an updater.
fragment = bytearray(body)
fragment[0x1000:0xf000] = bytes(0xe000)
for start, end in [(0x52b3, 0x530d), (0x53a3, 0x53d7),
                   (0xb000, 0xc800), (0xd404, 0xd41b)]:
    fragment[start:end] = body[start:end]

cases = {'renamed.exe': (body, True, True),
         'isolated-download-launch.exe': (fragment, True, False)}
text_section = bytearray(body)
pe_offset = struct.unpack_from('<I', body, 0x3c)[0]
section_offset = pe_offset + 24 + struct.unpack_from('<H', body, pe_offset + 20)[0]
text_section[section_offset:section_offset + 8] = b'.text\0\0\0'
cases['renamed-code-section.exe'] = (text_section, True, True)
for name, offset, value in [
        ('different-output-path.exe', 0x53cf, 0x28),
        ('different-extension-check-path.exe', 0x53b7, 0x30),
        ('different-control-transfer.exe', 0x5309, body[0x5309] + 1),
        ('wrong-resolver-import.exe', 0x52bb, 0x9c),
        ('wrong-launch-import.exe', 0x53d3, 0x7c),
        ('different-resolved-api.exe', 0xd419, ord('W'))]:
    changed = bytearray(body)
    changed[offset] = value
    cases[name] = (changed, False, False)

with tempfile.TemporaryDirectory(prefix='urlmon-cache-controls-', dir=args.output) as temporary:
    paths = []
    for name, (data, _, _) in cases.items():
        path = Path(temporary) / name
        path.write_bytes(data)
        paths.append(path)
    run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--no-update-check',
                          '--format', 'json', *map(str, paths)],
                         text=True, capture_output=True, check=True)
    (args.output / 'controls.stderr.txt').write_text(run.stderr)
    decoder, rest, reports = json.JSONDecoder(), run.stdout, []
    while rest.strip():
        report, end = decoder.raw_decode(rest.lstrip())
        rest = rest.lstrip()[end:]
        reports.append(report)
    files = {Path(file['path']).name: file for report in reports for file in report['files']}
    results = []
    for name, (_, capability, objective) in cases.items():
        ids = {t['id'] for t in files[name]['traits']}
        assert (CAPABILITY in ids) == capability, (name, 'capability', ids)
        assert (OBJECTIVE in ids) == objective, (name, 'objective', ids)
        results.append({'case': name, 'capability': capability, 'objective': objective, 'passed': True})
    (args.output / 'controls-results.json').write_text(json.dumps(results, indent=2) + '\n')
    (args.output / 'controls-reports.json').write_text(json.dumps(reports) + '\n')
print(f'PASS: {len(cases)} cache-path, API and intent-boundary controls')
