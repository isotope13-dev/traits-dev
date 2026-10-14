#!/usr/bin/env python3
"""pyproject/exe archive pooling must stay root-anchored.

`pyproject-package-with-exe` pools its legs across archive members, so a
monorepo source snapshot carrying a tooling pyproject.toml beside an
unrelated compiler-test Windows binary convicted the whole tree of
"Python-project package contains native binary". The composite now requires
the root-anchored `sdist-root-pyproject-toml` atom (like the setup.py
sibling's `sdist-root-setup-py`): a nested tooling recipe is inventory, not
a delivery shape.

Run `python3 testdata/pyproject-exe-pooling/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path testing suppressors
cannot mask the findings under test.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LEG = 'metadata/package/files/binary::pyproject-package-with-exe'
PARENT = ('metadata/package/files/binary::'
          'python-project-package-with-native-binary')
expected = {
    # Nested tooling recipe plus unrelated test binary: neither the
    # notable leg nor the suspicious parent may fire.
    'monorepo-snapshot-negative.zip': (set(), set()),
    # Flat distribution with a root build recipe beside a prebuilt
    # executable: both the notable leg and the suspicious parent fire,
    # and nothing hostile does.
    'flat-dist-positive.zip': ({LEG}, {PARENT}),
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for fixture in sorted(Path(__file__).parent.glob('*.zip')):
    target = scratch / fixture.name
    shutil.copyfile(fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    notable = set()
    suspicious = set()
    hostile = set()
    for entry in report['files']:
        for trait in entry['traits']:
            if trait['id'] == LEG:
                notable.add(fixture.name)
            if trait['id'] == PARENT:
                suspicious.add(fixture.name)
            if trait['crit'] == 5:
                hostile.add(trait['id'])
    assert hostile == set(), (fixture.name, sorted(hostile))
    want_leg, want_parent = expected[fixture.name]
    got_leg = {fixture.name} if notable else set()
    got_parent = {fixture.name} if suspicious else set()
    assert got_leg == (({fixture.name} if want_leg else set())), (
        fixture.name, sorted(got_leg))
    assert got_parent == (({fixture.name} if want_parent else set())), (
        fixture.name, sorted(got_parent))
    print(f'{fixture.name}: passed')
