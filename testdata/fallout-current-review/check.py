"""Static positive and near-miss checks; no specimen is executed."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GATE = 'objectives/anti-analysis/debugger-detect/combined-checks::python-analysis-exit'
BRANCH = 'micro-behaviors/process/exit/terminate::python-membership-systemexit-branch'
WARNING = 'micro-behaviors/process/debug/tool-markers::python-analysis-warning-reference'
NAME = 'metadata/binary/symbols/name/qualified::go-file-visit-routine'
CASES = {
    'gate.py': ([GATE, BRANCH, WARNING], []),
    'gate-no-message.py': ([GATE, BRANCH], [WARNING]),
    'gate-no-exit.py': ([WARNING], [GATE, BRANCH]),
    'gate-no-tools.py': ([BRANCH, WARNING], [GATE]),
    'gate-unconditional.py': ([], [GATE, BRANCH]),
    'warning-only.py': ([WARNING], [GATE, BRANCH]),
    'qualified-name.exe': ([NAME], []),
    'unqualified-name.exe': ([], [NAME]),
}
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER='')
run = subprocess.run(['atomscan', '--no-update', '--analyze', 'local',
                      '--follow=none', '--mode', 'slow', '-f', 'json',
                      *[str(HERE / name) for name in CASES]],
                     text=True, capture_output=True, env=env)
reports = [json.loads(line) for line in run.stdout.split('\n') if line.strip()]
actual = {Path(d['raw']['files'][0]['path']).name:
          {t['id'] for t in d['raw']['files'][0].get('traits', [])} for d in reports}
assert set(CASES) == set(actual), run.stderr
checks = 0
for name, (present, absent) in CASES.items():
    for trait in present:
        assert trait in actual[name], (name, 'missing', trait)
        checks += 1
    for trait in absent:
        assert trait not in actual[name], (name, 'unexpected', trait)
        checks += 1
print(f'PASS: {checks} assertions across {len(CASES)} static controls')
