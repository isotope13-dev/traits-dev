"""Run controls outside fixture paths, whose rules intentionally suppress LOLBins."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
root = Path(__file__).resolve().parent
scratch = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-e78afdd4/scratch')
cases = {'setup-slash.py': True, 'setup-dash.py': True,
         'local-registration.py': False, 'url-only.py': False}
rule = 'objectives/execution/lolbin/regsvr32::squiblydoo-plain'
hook = 'objectives/execution/lolbin/regsvr32::pypi-custom-install-regsvr32-scriptlet'
with tempfile.TemporaryDirectory(prefix='regsvr32-controls-', dir=scratch) as tmp:
    paths = {}
    for name in cases:
        dest = Path(tmp) / name.removesuffix('.py') / ('setup.py' if name.startswith('setup-') else 'main.py')
        dest.parent.mkdir()
        shutil.copyfile(root / name, dest)
        paths[str(dest)] = name
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'json', *paths],
                            capture_output=True, text=True, check=True)
    rest = result.stdout
    reports = []
    decoder = json.JSONDecoder()
    while rest.strip():
        data, end = decoder.raw_decode(rest.lstrip())
        reports.extend(data['files'])
        rest = rest.lstrip()[end:]
    seen = set()
    for f in reports:
        name = paths.get(f['path'])
        if name is None:
            continue
        traits = {t['id'] for t in f.get('traits', [])}
        wanted = cases[name]
        assert (rule in traits) == wanted, (name, rule, sorted(traits))
        assert (hook in traits) == wanted, (name, hook, sorted(traits))
        if name == 'local-registration.py':
            assert 'micro-behaviors/fs/path/application/executable::regsvr32-name-reference' in traits
        seen.add(name)
        print(name, 'PASS')
    assert seen == set(cases), seen

result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'json',
    *[str(root / name) for name in ['xor-cache.exe', 'or-cache.exe', 'xor-without-cache.exe']]],
    capture_output=True, text=True, check=True)
rest = result.stdout
while rest.strip():
    data, end = json.JSONDecoder().raw_decode(rest.lstrip())
    rest = rest.lstrip()[end:]
    for f in data['files']:
        name = Path(f['path']).name
        traits = {t['id'] for t in f.get('traits', [])}
        found = 'micro-behaviors/data/encoding/xor::v8-modulo-xor-indexed-store' in traits
        assert found == (name == 'xor-cache.exe'), (name, sorted(traits))
        print(name, 'PASS')
