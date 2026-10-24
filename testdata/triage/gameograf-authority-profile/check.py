#!/usr/bin/env python3
"""Check declared authority separately from inferred background search abuse."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
p.add_argument('--staging', type=Path, required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[2]
base = json.loads((here / 'manifest.json').read_text())
expected = {'full': (True, True), 'no-search': (False, False),
            'no-alarm': (True, False), 'other-author': (False, False)}
for name in expected:
    data = json.loads(json.dumps(base))
    if name == 'no-search': data['permissions'].remove('search')
    if name == 'no-alarm': data['permissions'].remove('alarms')
    if name == 'other-author': data['author'] = 'Example Publisher'
    dest = a.staging / name / 'manifest.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data))
for name in ['jquery-selector.js', 'jquery-html.js']:
    (a.staging / name).write_bytes((here / name).read_bytes())
r = subprocess.run([a.cleave, '--traits-dir', str(repo), '--format', 'jsonl',
                    str(a.staging)], text=True, capture_output=True, check=True)
seen = set()
for line in r.stdout.splitlines():
    for f in json.loads(line)['files']:
        if Path(f['path']).name.startswith('jquery-'):
            ids = {t['id']: t['crit'] for t in f.get('traits', [])}
            assert ids['metadata/lang/source/syntax/call/arguments::dollar-call-interpolated-link-field'] == 3
            assert all(v < 4 for v in ids.values()), (f['path'], ids)
            print('PASS', Path(f['path']).name)
            continue
        name = Path(f['path']).parent.name
        if name not in expected: continue
        seen.add(name)
        traits = {t['id']: t['crit'] for t in f.get('traits', [])}
        prefix = 'metadata/permission/extension-api::gameograf-newtab-'
        actual = (prefix + 'search-worker-declarations' in traits,
                  prefix + 'search-alarm-storage-declarations' in traits)
        assert actual == expected[name], (name, actual, expected[name])
        assert traits['metadata/permission/host/api.gameograf.com::declared'] == 3
        assert all(v < 4 for v in traits.values()), (name, traits)
        assert not any(k.startswith('well-known/unwanted/gameograf::') for k in traits)
        print('PASS', name)
assert seen == set(expected), seen
print('4 authority controls and 2 template controls passed')
