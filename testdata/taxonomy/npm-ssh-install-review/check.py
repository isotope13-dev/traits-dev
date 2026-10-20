#!/usr/bin/env python3
"""Check install-hook source/sink boundaries without executing the hooks."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
cases = json.loads((fixtures / 'cases.json').read_text())['cases']
# Stage under neutral directory names: path-based test suppressors must not
# make the negative controls pass or conceal the positive install hooks.
with tempfile.TemporaryDirectory(prefix='npm-ssh-controls-', dir=root) as temp:
    paths = []
    for index, case in enumerate(cases):
        basename = 'package.json' if case['path'].endswith('.json') else 'source.cs'
        target = Path(temp) / str(index) / basename
        target.parent.mkdir()
        shutil.copyfile(root / case['path'], target)
        paths.append(str(target))
    result = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--format', 'json', *paths],
        text=True, capture_output=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout
    observed = {}
    while remaining.strip():
        report, consumed = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[consumed:]
        for file in report['files']:
            observed[file['path']] = {t['id']: t['crit'] for t in file['traits']}
    for path, case in zip(paths, cases):
        traits = observed[path]
        missing = set(case['required']) - traits.keys()
        forbidden = set(case['forbidden']) & traits.keys()
        assert not missing and not forbidden, (case['id'], missing, forbidden)
        if case['id'] == 'fake-key':
            assert sum(c == 5 for c in traits.values()) == 0, traits
            assert sum(c == 4 for c in traits.values()) == 1, traits
        if case['id'] == 'private-key-fallback':
            assert sum(c == 5 for c in traits.values()) == 2, traits
        print('PASS:', case['id'])
print('PASS:', len(cases), 'SSH install controls')
