#!/usr/bin/env python3
"""Check dotfile call evidence outside test-directory suppressors.

Usage: python3 testdata/cjs-dotfile-require/check.py <scratch-directory>
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

fixtures = Path(__file__).resolve().parent
root = fixtures.parents[1]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
trait_id = 'micro-behaviors/os/module/load::cjs-dotfile-require'
expected = {
    'local-dotfiles.js': True,
    'local-dotfiles.ts': True,
    'ordinary-paths.js': False,
    'quoted-require.js': False,
    'mixed.js': True,
}
targets = []
for name in expected:
    target = scratch / name
    shutil.copyfile(fixtures / name, target)
    targets.append(str(target))
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'jsonl', *targets],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), capture_output=True,
    text=True, check=True,
)
# Reports may be concatenated JSON objects. Split with the JSON decoder so
# escaped source and Unicode line separators cannot become record boundaries.
pending = result.stdout.lstrip()
decoder = json.JSONDecoder()
seen = set()
while pending:
    report, end = decoder.raw_decode(pending)
    pending = pending[end:].lstrip()
    for entry in report['files']:
        name = Path(entry['path']).name
        if name not in expected:
            continue
        seen.add(name)
        matches = [t for t in entry.get('traits', []) if t['id'] == trait_id]
        assert bool(matches) == expected[name], (name, matches)
        assert all(t['crit'] == 3 for t in matches), (name, matches)
        assert not any(t['id'].startswith(
            'objectives/supply-chain/trojanized/campaign::')
            for t in entry.get('traits', [])), name
        print(name + ': passed')
assert seen == set(expected), seen
