#!/usr/bin/env python3
"""Vendor release-policy verbs must not read as concealment (see README).

Run `python3 testdata/no-review-policy-verbs/check.py <scratch-directory>`.
`negative-policy.md` (vendor disclaimer) must not report the
`repository-content-agent-prompt-injection` composite;
`positive-directive.md` (addressed, imperative, unreviewed agent action)
must still report it.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RULE = ('objectives/evasion/security-bypass/llm/prompt/override::'
        'repository-content-agent-prompt-injection')
expected = {
    'negative-policy.md': False,
    'negative-approval-demand.md': False,
    'positive-directive.md': True,
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for name, want in sorted(expected.items()):
    target = scratch / name
    shutil.copyfile(Path(__file__).parent / name, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    seen = {t['id'] for e in report['files'] for t in e.get('traits', [])}
    got = RULE in seen
    assert got == want, (name, sorted(seen))
    print(f'{name}: passed')
