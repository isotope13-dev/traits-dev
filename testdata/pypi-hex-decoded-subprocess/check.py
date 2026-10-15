#!/usr/bin/env python3
"""Hex-decoded subprocess execution in setup.py must convict twice.

`pypi-install-hex-decoded-subprocess` (install-time decoded exec) and
`pypi-sysargv-gated-decoded-subprocess` (argv-gated decoded exec) must both
fire on a setup.py that hex-decodes a gate token and a command and runs the
command when the token appears in sys.argv. Either leg alone (a build probe
without decoding, a hex constant without execution) must not convict.

Run `python3 testdata/pypi-hex-decoded-subprocess/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path suppressors cannot mask the
findings under test. Each fixture keeps the `setup.py` basename one directory
deep so the `root-setup-py` install context leg still applies.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

H1 = ('objectives/supply-chain/install-hook/setup::'
      'pypi-install-hex-decoded-subprocess')
H2 = ('objectives/supply-chain/install-hook/dropper/hook-setup::'
      'pypi-sysargv-gated-decoded-subprocess')
LEGS = {
    'metadata/build/pip::root-setup-py',
    'micro-behaviors/data/decode/hex::python-fromhex',
    'micro-behaviors/process/create/subprocess::run-ast',
    'micro-behaviors/process/argument/subcommand::'
    'python-sys-argv-membership-test',
}
expected = {
    # Gated decoded exec: both hostile verdicts present, all legs live.
    'positive': ({H1, H2}, LEGS),
    # Build probe without decoding: subprocess legs live, no verdict.
    'negative-build-probe': (set(), {
        'metadata/build/pip::root-setup-py',
        'micro-behaviors/process/create/subprocess::run-ast',
    }),
    # Hex constant without execution: decode leg live, no verdict.
    'negative-hex-constant': (set(), {
        'metadata/build/pip::root-setup-py',
        'micro-behaviors/data/decode/hex::python-fromhex',
    }),
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for case in sorted(expected):
    fixture = Path(__file__).parent / case / 'setup.py'
    target_dir = scratch / case
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fixture, target_dir / 'setup.py')
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target_dir / 'setup.py')],
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
    want_hostile, want_legs = expected[case]
    assert hostile == want_hostile, (case, sorted(hostile))
    missing = want_legs - seen
    assert not missing, (case, sorted(missing))
    print(f'{case}: passed')
