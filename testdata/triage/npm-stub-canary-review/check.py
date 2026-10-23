#!/usr/bin/env python3
"""Focused source/sink and relocation controls; never execute fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GET = 'micro-behaviors/communications/http/get::node-base64-buffer-get-url'
ENC = 'micro-behaviors/data/encode/base64::node-json-base64-with-host-query'
SMALL = 'metadata/lang/source/syntax/assignment::small-commonjs-object-export'
EMPTY = 'metadata/lang/source/syntax/assignment::commonjs-empty-object-export'
CASES = {
    'buffer-url.js': ({GET}, {ENC}),
    'unrelated-buffer.js': ({ENC}, {GET}),
    'hex-url.js': (set(), {GET, ENC}),
    'fake-client.js': (set(), {GET, ENC}),
    'host-record.js': ({ENC}, {GET}),
    'object-export.js': ({SMALL, EMPTY}, {GET, ENC}),
    'helper-export.js': ({SMALL}, {EMPTY, GET, ENC}),
}

for filename, (present, absent) in CASES.items():
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(HERE / filename)],
        text=True, capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    traits = {trait['id']: trait['crit']
              for file in report['files'] for trait in file.get('traits', [])}
    assert present <= traits.keys(), (filename, 'missing', present - traits.keys())
    assert not absent.intersection(traits), (filename, 'unexpected', absent.intersection(traits))
    assert not [t for t, crit in traits.items() if crit >= 4], (filename, 'unsupported suspicion')
    print(f'PASS {filename}')

attack = ROOT / 'testdata/hostile/host-json-base64-oast-profile.js'
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', str(attack)], text=True, capture_output=True, check=True,
)
traits = {trait['id']: trait['crit'] for file in json.loads(result.stdout)['files']
          for trait in file.get('traits', [])}
assert traits.get('objectives/supply-chain/recon-exfil/oast/secret::node-oastify-https-profile-exfil') == 5
assert traits.get(ENC) == 3
assert traits.get(GET) == 3
print('PASS retained hostile host-profile export')
