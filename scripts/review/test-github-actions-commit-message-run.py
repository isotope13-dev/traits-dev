#!/usr/bin/env python3
"""Keep direct runner substitutions distinct from safely bound environment values."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'metadata/build/ci/expression::workflow-commit-message-inline-run'
PREFIX = '''name: CI
on: [push]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
'''
EXPRESSION = '${{ github.event.head_commit.message }}'
cases = [
    ('direct', PREFIX + '      - run: echo "' + EXPRESSION + '"\n', True),
    ('block', PREFIX + '      - run: |\n          echo "' + EXPRESSION + '"\n', True),
    ('environment', PREFIX + '      - run: echo "$MESSAGE"\n        env:\n          MESSAGE: ' + EXPRESSION + '\n', False),
    ('step_name', PREFIX + '      - name: ' + EXPRESSION + '\n        run: echo hello\n', False),
    ('different_field', PREFIX + '      - run: echo "${{ github.sha }}"\n', False),
]
with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp) / '.github' / 'workflows'
    directory.mkdir(parents=True)
    for name, source, expected in cases:
        path = directory / (name + '.yml')
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('GitHub Actions commit-message run boundaries passed')
