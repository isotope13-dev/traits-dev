"""Check static findings; never execute the AppleScript or command fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
PUT = 'micro-behaviors/communications/http/put::curl-put-command'
SIGN = 'micro-behaviors/crypto/sign::wallet-asar-copy-adhoc-context'
REPLACE = ('objectives/supply-chain/trojanized/app/wallet::'
           'wallet-resource-phish-replacement')
EXPECTED = {
    'maintenance.applescript': {SIGN: 3},
    'sign-only.applescript': {},
    'renamed-collector.applescript': {SIGN: 3, PUT: 3, REPLACE: 5},
    'put.sh': {PUT: 3},
    'put-long.py': {PUT: 3},
    'put-short.js': {PUT: 3},
    'post.sh': {},
    'put-in-data.sh': {},
    'put-prefix.sh': {},
    'put-as-data-option.sh': {},
    'put-hyphen.sh': {},
}


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        yield value
        text = text.lstrip()[end:]


parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path,
                    help='Check an already captured Cleave JSON report')
args = parser.parse_args()
if args.report:
    output = args.report.read_text()
else:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *[str(BASE / name) for name in EXPECTED]],
        env={**os.environ, 'CLEAVE_NO_UPDATE_CHECK': '1'},
        capture_output=True, text=True, check=True)
    output = result.stdout

seen = set()
for report in documents(output):
    for file in report['files']:
        name = Path(file['path']).name
        if name not in EXPECTED:
            continue
        findings = {t['id']: t['crit'] for t in file.get('traits', [])}
        actual = {k: findings[k] for k in (PUT, SIGN, REPLACE) if k in findings}
        assert actual == EXPECTED[name], (name, actual, EXPECTED[name])
        assert not any(k.startswith('objectives/evasion/masquerade/process/'
                                    'app-substitute::wallet-resource-')
                       for k in findings), name
        seen.add(name)
assert seen == EXPECTED.keys(), (seen, EXPECTED.keys())
print(f'{len(seen)} static controls passed')
