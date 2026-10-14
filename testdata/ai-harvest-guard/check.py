#!/usr/bin/env python3
"""AI coding-tool secret-harvest must need two collection roles.

`ai-coding-tool-secret-harvest` convicted a file that named AI-tool config
directories, walked trees, and mentioned key shapes: a push-wall guard that
REFUSES such paths. One of its two required `any` legs was the baseline
`.key` extension string (conf 0.5), which exclusion lists, archive
validators, and docs all contain. The leg was removed from the hostile
threshold: each remaining leg (repeated reads, two kinds of credential
files, a PEM reference) establishes a distinct collection role.

Run `python3 testdata/ai-harvest-guard/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path testing suppressors
cannot mask the findings under test. The scratch directory itself must
not contain test-like path tokens (`test`, `spec`, ...): the directory-walk
legs carry a test-harness suppressor, and a test-named scratch would make
both fixtures vacuous. This script refuses such paths outright.
`negative-guard.js` (guard shape: config-dir list, repeated walks, a `.key`
exclusion string, no credential reads) must report no hostile findings
while still reporting the walk, config-cluster, and readdir legs that prove
the shape is live. `positive-stealer.js` (config-dir list, repeated walks,
credential file kinds) must still report the harvest verdict.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HARVEST = ('objectives/credential-access/dev-tools/ai::'
           'ai-coding-tool-secret-harvest')
WALK = 'micro-behaviors/fs/directory/traverse::node-dirent-directory-walk'
CLUSTER = ('micro-behaviors/fs/path/agent-config/directory::'
           'ai-coding-tool-config-directory-cluster')
READDIR = 'micro-behaviors/fs/directory/readdir::node-readdir-repeated'
expected = {
    # Guard shape: legs live, hostile verdict absent.
    'negative-guard.js': (set(), {WALK, CLUSTER, READDIR}),
    # Stealer shape: legs live, hostile verdict present.
    'positive-stealer.js': ({HARVEST}, {WALK, CLUSTER, READDIR}),
}

scratch = Path(sys.argv[1])
if re.search(r'test|spec', str(scratch), re.I):
    sys.exit(f'refusing test-like scratch path (would suppress walk legs): '
             f'{scratch}')
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for fixture in sorted(Path(__file__).parent.glob('*.js')):
    target = scratch / fixture.name
    shutil.copyfile(fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    hostile = set()
    seen = set()
    for entry in report['files']:
        for trait in entry['traits']:
            if trait['crit'] == 5:
                hostile.add(trait['id'])
            seen.add(trait['id'])
    want_hostile, want_legs = expected[fixture.name]
    assert hostile == want_hostile, (fixture.name, sorted(hostile))
    missing = want_legs - seen
    assert not missing, (fixture.name, sorted(missing))
    print(f'{fixture.name}: passed')
