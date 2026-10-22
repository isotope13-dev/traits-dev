#!/usr/bin/env python3
"""Static-only controls for credential envelopes, procfs globs and x86 hooks."""
import argparse
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--samples', required=True, type=Path)
parser.add_argument('--scratch', required=True, type=Path)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = args.scratch / 'controls'
fixtures.mkdir(parents=True, exist_ok=True)
source = (args.samples / '166889ed606a/sitecustomize.py').read_text()
upload = 'micro-behaviors/communications/http/upload::python-credential-dictionary-encrypted-post'
exfil = 'objectives/exfiltration/stealer/credential::python-credential-http-upload'
glob = 'micro-behaviors/fs/proc/info/path::python-proc-environ-glob'
hook = 'micro-behaviors/hardware/input/keyboard/hook::x86-iat-low-level-keyboard-hook'
group = 'micro-behaviors/hardware/input/keyboard/hook::windows-keyboard-hook-install'
cases = {}


def fixture(name, data, required=(), forbidden=()):
    path = fixtures / name
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    cases[str(path.resolve())] = (set(required), set(forbidden))


fixture('collector.py', source, [upload, exfil, glob])
renamed = source
for old, new in {'secrets': 'bundle', 'target': 'item', 'relative': 'entry',
                 'plaintext': 'compressed', 'encrypted': 'cipherbytes',
                 'cipher': 'aes_cipher', 'wrapped': 'envelope',
                 'response': 'reply', 'collect': 'gather'}.items():
    renamed = re.sub(r'\b' + old + r'\b', new, renamed)
fixture('renamed.py', renamed, [upload, exfil, glob])
fixture('httpx.py', source.replace('requests', 'httpx'), [upload, exfil])
fixture('old-numeric-glob.py', source.replace("'*/environ'", "'[0-9]*/environ'"), [upload, exfil, glob])
for name, old, new in [
    ('overwritten-plain.py', '    key = get_random_bytes', "    plaintext = b'public'\n    key = get_random_bytes"),
    ('overwritten-cipher.py', '    wrapped = ', "    encrypted = b'public'\n    wrapped = "),
    ('overwritten-dictionary.py', '    plaintext = ', '    secrets = {}\n    plaintext = '),
    ('unrelated-dictionary.py', 'json.dumps(secrets)', 'json.dumps(public_data)'),
    ('unrelated-read.py', 'target.read_text(', 'other.read_text('),
    ('unrelated-post.py', 'data=wrapped + iv + encrypted', "data=b'public'"),
    ('overwritten-wrapped.py', '    wrapped = ', '    encrypted = '),
    ('noncredential-paths.py', "('.aws/credentials', '.kube/config', '.npmrc', '.pypirc', '.git-credentials', '.netrc', '.ssh/id_rsa', '.ssh/id_ed25519')", "('public.json', 'public.txt')"),
]:
    assert old in source, name
    fixture(name, source.replace(old, new), forbidden=[upload, exfil])
fixture('quoted.py', repr(source) + '\n', forbidden=[upload, exfil])
fixture('different-proc-file.py', "from pathlib import Path\nPath('/proc').glob('*/cmdline')\n", forbidden=[glob])
fixture('different-root.py', "from pathlib import Path\nPath('/sys').glob('*/environ')\n", forbidden=[glob])
fixture('public-upload.py', "import requests\nrequests.post('https://example.org/upload', data=open('public.txt', 'rb').read())\n", forbidden=[upload, exfil, glob])

binary = (args.samples / '7e224fcf3553/7e224fcf35535e12b6bd526cff7e232f2ff8a71c99f77512bb678c4dde16b539').read_bytes()
fixture('keyboard.exe', binary, [hook, group])
mouse = bytearray(binary)
assert mouse[0x4562:0x4564] == b'\x6a\x0d'
mouse[0x4563] = 14  # WH_MOUSE_LL: the IAT target and callback remain unchanged.
fixture('mouse.exe', mouse, forbidden=[hook, group])
for name in ['keylog-dropper-controls.exe']:
    fixture(name, (root / 'testdata/benign' / name).read_bytes(), forbidden=[hook, group])

scan = subprocess.run([args.cleave, '--traits-dir', str(root), '--json', str(fixtures)],
                      capture_output=True, text=True, check=True)
(args.scratch / 'controls.jsonl').write_text(scan.stdout)
(args.scratch / 'controls.log').write_text(scan.stderr)
reports = {}
for line in scan.stdout.splitlines():
    for item in json.loads(line).get('files', []):
        path = str(Path(item['path']).resolve())
        reports[path] = {t['id'] for t in item.get('traits', [])}
failures = []
for path, (required, forbidden) in cases.items():
    found = reports.get(path)
    if found is None:
        failures.append(f'{path}: missing report')
    elif required - found or forbidden & found:
        failures.append(f'{path}: missing={sorted(required-found)} unexpected={sorted(forbidden & found)}')
if failures:
    raise SystemExit('\n'.join(failures))
print(f'PASS: {len(cases)} static controls')
