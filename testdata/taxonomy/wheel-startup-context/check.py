"""Static wheel startup-context controls; source snippets are never executed."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OLD = 'objectives/supply-chain/recon-exfil/runtime::pypi-wheel-pth-startup-host-recon-snapshot'
NEW = 'micro-behaviors/process/interpreter/python::wheel-pth-metadata-json-context'

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cleave', default='cleave')
p.add_argument('--before', action='store_true')
p.add_argument('--artifacts', type=Path)
a = p.parse_args()

# This import hook builds an in-memory diagnostic report. There is no local
# snapshot write, metadata request, upload, secret targeting or concealed code.
source = '''import os, json
headers = {"Metadata-Flavor": "Google"}
def summarize():
    return json.dumps({"host": "diagnostic", "names": list(os.environ.items())})
summarize()
'''
with tempfile.TemporaryDirectory() as temp:
    work = a.artifacts or Path(temp)
    work.mkdir(parents=True, exist_ok=True)
    cases = {
        'diagnostic-1.0-py3-none-any.whl': {'diagnostic.pth': 'import diagnostic\n', 'diagnostic.py': source},
        'split-1.0-py3-none-any.whl': {'split.pth': 'import harmless\n', 'harmless.py': 'pass\n', 'unrelated.py': source},
        'path-only-1.0-py3-none-any.whl': {'path-only.pth': 'support\n', 'diagnostic.py': source},
        'no-survey-1.0-py3-none-any.whl': {'no-survey.pth': 'import harmless\n', 'harmless.py': 'pass\n'},
    }
    for name, files in cases.items():
        path = work / name
        with zipfile.ZipFile(path, 'w') as z:
            for member, text in files.items():
                z.writestr(member, text)
            z.writestr('diagnostic-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: diagnostic\nVersion: 1.0\n')
        result = subprocess.check_output([a.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(path)], text=True)
        report = json.loads(result)
        findings = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        expected = name.startswith(('diagnostic-', 'split-'))
        target = OLD if a.before else NEW
        assert (target in findings) == expected, (name, target, findings)
        if not a.before:
            assert OLD not in findings
            assert findings.get(NEW, 3) == 3, (name, findings.get(NEW))
            assert not any(level >= 4 for level in findings.values()), (name, findings)
        print(name, target in findings, findings.get(target))
print('4 static startup-context controls passed')
