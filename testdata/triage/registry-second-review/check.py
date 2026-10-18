"""Focused behavioral controls; optional --sample checks the original stealer."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
parser.add_argument('--sample', type=Path)
args = parser.parse_args()
folder = Path(__file__).resolve().parent
root = folder.parents[2]
fixtures = [folder / name for name in (
    'coercion-typeerror.html', 'json-export-only.js',
    'unrelated-json-record.js', 'token-format-only.js', 'substitution-jsfuck-loader.html')]
if args.sample:
    fixtures.append(args.sample.resolve())
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                         *map(str, fixtures)], text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stderr or result.stdout)
assert not result.stderr.strip(), result.stderr
remaining = result.stdout
reports = {}
while remaining.strip():
    report, length = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[length:]
    reports.update({Path(f['path']).name: f for f in report['files']})
schema = 'micro-behaviors/data/serialize/schema-credential::fetch-json-browser-secret-fields'
parser_formats = 'micro-behaviors/data/format/credentials::discord-token-parser-formats'
for fixture in fixtures[:5]:
    traits = reports[fixture.name]['traits']
    assert not any(t['crit'] == 5 for t in traits), fixture.name
    if fixture.suffix != '.html':
        assert not any(t['crit'] == 4 for t in traits), fixture.name
assert schema in {t['id'] for t in reports['json-export-only.js']['traits']}
assert schema not in {t['id'] for t in reports['unrelated-json-record.js']['traits']}
assert parser_formats in {t['id'] for t in reports['token-format-only.js']['traits']}
if args.sample:
    traits = reports[args.sample.name]['traits']
    assert sum(t['crit'] == 5 for t in traits) >= 2
    assert 'objectives/exfiltration/stealer/browser::node-browser-decryption-secret-export' in {t['id'] for t in traits}
print('PASS: coercion, format-only, JSON export, and credential theft controls')
