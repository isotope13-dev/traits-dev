"""Focused regression controls: neutral provider versus credential exfiltration."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AWS = 'micro-behaviors/communications/http/services/aws::node-ecs-relative-credential-endpoint-reference'
TOKEN = 'micro-behaviors/data/string/concat::go-token-keyword-concatenation'
URL = 'micro-behaviors/communications/http/url/external-ip::data-http-ip-port-reference'
EVAL = 'micro-behaviors/process/interpreter/eval/direct::vbs-execute-statement'
EXFIL = 'objectives/supply-chain/recon-exfil/registry/probe::node-install-ecs-iam-credential-exfil'
CASES = {
    'provider.js': ({AWS}, {EXFIL}),
    'provider-nearmiss.js': (set(), {AWS, EXFIL}),
    'exfil.js': ({AWS, EXFIL}, set()),
    'token.go': ({TOKEN}, set()),
    'token-nearmiss.go': (set(), {TOKEN}),
    'reference.dat': ({URL}, set()),
    'reference-nearmiss.dat': (set(), {URL}),
    'evaluation.vbs': ({EVAL}, set()),
    'evaluation-nearmiss.vbs': (set(), {EVAL}),
}
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_SKIP_CACHE='1')
result = subprocess.run(['atomscan', '--no-update', '--mode', 'slow', '--follow=none', '-f', 'json', *[str(HERE / f) for f in CASES]], env=env, capture_output=True, text=True)
assert result.returncode in (0, 1), result.stderr
assert not any(s in result.stderr for s in ("Failed to load traits", "validation failed", "error analyzing")), result.stderr
seen = set()
for line in result.stdout.splitlines():
    report = json.loads(line)['raw']
    assert report['files'], 'empty analysis'
    file = report['files'][0]
    name = Path(file['path']).name
    ids = {t['id'] for t in file.get('traits', [])}
    wanted, absent = CASES[name]
    assert wanted <= ids, (name, 'missing', wanted - ids)
    assert not absent & ids, (name, 'unexpected', absent & ids)
    if name != 'exfil.js':
        limit = 5 if name == 'evaluation.vbs' else 4
        assert not [t for t in file.get('traits', []) if t['crit'] >= limit], name
    seen.add(name)
assert seen == CASES.keys(), ('missing reports', CASES.keys() - seen)
print(f'{len(seen)} positive and near-miss controls passed')
