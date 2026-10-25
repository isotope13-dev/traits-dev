"""Inspect static matcher results; never execute the fixture programs."""
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LIST = 'micro-behaviors/fs/directory/readdir::applescript-list-folder-assignment'
CWD = 'micro-behaviors/fs/directory/cwd::perl-cwd-word-reference'
BROWSE = 'micro-behaviors/fs/directory/readdir::directory-browser'
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_NO_UPDATE_CHECK='1')
cases = [
    ('list.applescript', [LIST], []),
    ('embedded.py', [LIST], []),
    ('near-miss.applescript', [], [LIST]),
    ('cwd.pl', [CWD], [BROWSE]),
    ('cwd-word.pl', [CWD], [BROWSE]),
    ('no-cwd.pl', [], [CWD, BROWSE]),
]
checks = 0
for name, present, absent in cases:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         'test-rules', '--rules', ','.join(present + absent), str(HERE / name)],
        env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'Warning:' not in result.stderr, result.stderr
    matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.M))
    assert set(present) <= matched, (name, present, result.stdout)
    assert not set(absent) & matched, (name, absent, result.stdout)
    checks += len(present) + len(absent)
print(f'{checks} assertions passed across {len(cases)} cases')
