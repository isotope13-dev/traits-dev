#!/usr/bin/env python3
"""Recognize calls to a Git helper with staged-diff arguments."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = "async function f(root, files){ return await git(root, ['diff', '--cached', '--', ...files]); }\n"
cases = {'staged.js': source, 'status.js': source.replace("'diff'", "'status'"),
         'unstaged.js': source.replace("'--cached'", "'--stat'"),
         'other.js': source.replace('await git(', 'await other(')}
with tempfile.TemporaryDirectory(prefix='node-staged-diff-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    trait = 'micro-behaviors/revision-control/git/read::node-git-helper-staged-diff'
    assert trait in found['staged.js']
    assert all(trait not in found[n] for n in cases if n != 'staged.js')
    print('Staged diff finding requires Git helper, diff and --cached.')
