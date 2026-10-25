#!/usr/bin/env python3
"""Static regression checks; sample code is only passed to cleave."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
paths = [HERE / name for name in (
    'native-env.c', 'native-env-upload.c', 'python-mapping.c',
    'autostart-reason.py', 'command-safety.py', 'hosted-wheel.py',
    'distant-host.py',
)]
paths += [ROOT / name for name in (
    'testdata/dtls-fragment-accounting/changed-count.js',
    'testdata/dtls-fragment-accounting/ordinary-fragments.py',
    'testdata/dtls-fragment-accounting/unrelated-length.py',
    'testdata/hostile/python-silent-native-stage-controls.py',
    'testdata/hostile/corpus-with-executable-reverse-shell.js',
    'testdata/benign/codeam-second-review/local-pty.py',
)]
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', *map(str, paths)],
    check=True, text=True, capture_output=True,
)
remaining = result.stdout.lstrip()
files = {}
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        files[Path(file['path']).name] = {
            trait['id']: trait['crit'] for trait in file.get('traits', [])
        }

def has(name, trait):
    return trait in files[name]

env = 'micro-behaviors/os/env/read::native-environ-reference'
guard = 'micro-behaviors/process/create/shell/guard::agent-guard-command-safety'
host = 'micro-behaviors/communications/http/services/file-hosting::wheel-url-near-file-host'
assert has('native-env.c', env)
assert has('native-env-upload.c', env)
assert has('native-env-upload.c', 'objectives/exfiltration/stealer/env::native-http-host-profile-exfil')
assert not has('python-mapping.c', env)
assert has('command-safety.py', guard)
assert not has('autostart-reason.py', guard)
assert has('hosted-wheel.py', host)
assert not has('distant-host.py', host)
assert files['hosted-wheel.py'][host] == 3
assert not any(c >= 4 for c in files['hosted-wheel.py'].values())
dtls = 'objectives/lateral-movement/exploit/memory::padded-fragment-accounting-overflow'
assert has('changed-count.js', dtls)
assert not has('ordinary-fragments.py', dtls)
assert not has('unrelated-length.py', dtls)
assert has('python-silent-native-stage-controls.py', 'objectives/supply-chain/hidden-payload/native-extension::python-fail-open-unverified-native-stage')
assert has('corpus-with-executable-reverse-shell.js', 'objectives/command-and-control/reverse-shell/dev-tcp::node-executes-bash-tcp-shell')
assert not any(c >= 4 for c in files['local-pty.py'].values())
print('PASS: 13 static controls, retained native-env upload, DTLS, stager and reverse shell')
