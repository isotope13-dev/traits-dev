"""Scan fixture bytes without executing the managed or PowerShell examples."""
import json
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
RULES = {
    'managed': 'micro-behaviors/os/module/load::python-loaded-assembly-method-invocation',
}
CASES = {
    'managed-invoke.py': True,
    'managed-lookup-only.py': False,
    'managed-unrelated-invoke.py': False,
    'managed-other-loader.py': False,
    'managed-rebound-method.py': False,
}
env = os.environ.copy()
for key in ['CLEAVE_VALIDATE', 'SCAN_HOPPER', 'SCAN_FETCH', 'SCAN_LLM', 'SCAN_REGISTRY_MAP']:
    env.pop(key, None)
env['CLEAVE_TRAITS_DIR'] = str(ROOT.parent.parent)
result = subprocess.run(
    ['atomscan', '--no-update', '--analyze', 'local', '--mode', 'slow',
     '--follow=none', '-f', 'json', *[str(ROOT / name) for name in CASES]],
    env=env, capture_output=True, text=True,
)
assert result.returncode in [0, 1], result.stderr
reports = {
    pathlib.Path(report['raw']['files'][0]['path']).name: report
    for report in map(json.loads, result.stdout.splitlines())
}
for name, expected in CASES.items():
    ids = {t['id'] for f in reports[name]['raw']['files'] for t in f.get('traits', [])}
    rule = RULES['managed']
    assert (rule in ids) == expected, (name, expected, ids)
    print('PASS', name)
