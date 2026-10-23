#!/usr/bin/env python3
"""Check Basic auth coverage, WAN exploit controls, and response relocation."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
auth = 'micro-behaviors/communications/http/auth::basic-authorization-concatenated-value'
binding = 'micro-behaviors/communications/http/client/exchange::urllib-urlopen-bound-as-response'
old_binding = 'micro-behaviors/communications/http/download/write::urllib-urlopen-bound-as-response'
download = 'micro-behaviors/communications/http/download/write::python-urlopen-script-write-profile'
acquisition = 'micro-behaviors/communications/http/client/response-body::http-response-acquisition'
wan = 'objectives/execution/exploit/http-command-injection::wan-form-username-'
hostile = {wan + 'shell-injection', wan + 'comment-suppression'}
cases = []
for path in sorted((root / 'testdata/hostile/wan-credential-injection').glob('*')):
    required = set(hostile)
    if path.name == 'setwan-ppp.py':
        required |= {auth, binding}
    elif path.name == 'setwan-pptp.js':
        required.add(auth)
    cases.append((path, required, {old_binding, download}))
for path in sorted((root / 'testdata/benign/wan-credential-injection').glob('*')):
    cases.append((path, set(), hostile))
for path in sorted((root / 'testdata/suspicious/wan-credential-injection').glob('*')):
    suffix = 'newline-command-redirect' if path.name == 'setwan-newline.py' else 'shell-substitution-redirect'
    cases.append((path, {'objectives/execution/exploit/command-injection::username-field-' + suffix}, hostile))
for name in ['basic-python.py', 'basic-javascript.js']:
    cases.append((here / name, {auth}, hostile))
cases.append((here / 'auth-near-miss.py', set(), {auth} | hostile))
# The shared download rule excludes test paths. Run its positive outside that
# exclusion as well as inspecting the existing corpus controls in place.
temporary = tempfile.TemporaryDirectory(prefix='wan-response-control-', dir=args.scratch)
saved_source = Path(temporary.name) / 'save-response.py'
saved_source.write_text((here / 'save-response.py').read_text())
cases.append((saved_source, {binding, download}, {old_binding}))
# Independent existing positive and benign controls: neither merely binding a
# response nor retaining the unsafe-YAML finding requires saving a file.
cases.append((root / 'testdata/hostile/yaml-unsafe-fetch-dropper.py', {binding}, {old_binding, download}))
cases.append((root / 'testdata/calibration-first-review/normal-form.py', {binding}, hostile | {old_binding, download}))
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--json', 'analyze']
    + [str(path) for path, _, _ in cases], capture_output=True, text=True, check=True)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line).get('files', []):
        reports[file['path']] = {t['id'] for t in file.get('traits', [])}
for path, required, absent in cases:
    seen = reports.get(str(path), set())
    assert not required - seen, (str(path), 'missing', sorted(required - seen))
    assert not absent & seen, (str(path), 'unexpected', sorted(absent & seen))
# Pure any-groups are intentionally omitted from normal findings. Exercise
# evaluation directly so the moved observation still feeds ancestor consumers.
trace = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), 'test-rules',
     str(root / 'testdata/hostile/wan-credential-injection/setwan-ppp.py'),
     '--rules', acquisition], capture_output=True, text=True, check=True)
assert 'MATCHED ' + acquisition in trace.stdout, trace.stdout + trace.stderr
temporary.cleanup()
print(f'PASS: {len(cases)} WAN, authentication, and response controls')
