#!/usr/bin/env python3
"""Static controls derived from a supplied npm sample; never load its code."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
with tarfile.open(args.sample) as archive:
    entries = {entry.name: archive.extractfile(entry).read()
               for entry in archive.getmembers() if entry.isfile()}
addon = next(name for name in entries if name.endswith('.node'))
original = entries[addon]
secret_names = [b'AWS_ACCESS_KEY_ID', b'AWS_SECRET_ACCESS_KEY',
                b'AWS_SESSION_TOKEN', b'GITHUB_TOKEN', b'NPM_TOKEN',
                b'NODE_AUTH_TOKEN', b'SYSTEM_ACCESSTOKEN',
                b'ACTIONS_RUNTIME_TOKEN', b'ACTIONS_ID_TOKEN_REQUEST_TOKEN']
variants = {}
# No endpoint label, package identifier, native filename, directory or release
# number should be required to convict an unchanged secret-export mechanism.
renamed = {}
for name, content in entries.items():
    if name.endswith('package.json'):
        manifest = json.loads(content)
        manifest.update(name='@example/runtime', version='1.2.3')
        manifest['files'] = ['index.js', 'assets']
        content = json.dumps(manifest).encode()
    elif name.endswith('index.js'):
        content = content.replace(b'prebuilds', b'assets').replace(
            b'metrics.node', b'monitor.node').replace(
            b'@brick-v2/core', b'@example/runtime')
    elif name == addon:
        content = content.replace(b'oob.s4yhii.com', b'api.server.com')
        assert len(content) == len(original)
        name = name.replace('prebuilds', 'assets').replace('metrics.node', 'monitor.node')
    renamed[name] = content
variants['renamed-endpoint-and-layout'] = renamed
neutral = dict(entries)
for name in secret_names:
    neutral[addon] = neutral[addon].replace(name, b'X' * len(name))
variants['host-report-without-credential-targets'] = neutral
# Removing network send evidence must leave individual secret names and native
# loading visible, but cannot establish the source-to-send objective.
no_send = dict(entries)
no_send[addon] = original.replace(b'send\0', b'noop\0')
variants['without-send-evidence'] = no_send
for variant, members in variants.items():
    with tarfile.open(args.output / (variant + '.tgz'), 'w:gz') as archive:
        for name, content in members.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(content)
            archive.addfile(entry, io.BytesIO(content))
# Scan the original and every control in one process so they share one ruleset.
environment = dict(os.environ, SCAN_FETCH='none', CLEAVE_VALIDATE='0', SCAN_NO_UPDATE='1')
environment.pop('SCAN_HOPPER', None)
environment.pop('SCAN_REGISTRY_MAP', None)
paths = [args.sample, *(args.output / (name + '.tgz') for name in variants)]
result = subprocess.run(['atomscan', '--no-update', '--mode', 'slow', '-f', 'json',
                         *(str(path) for path in paths)], env=environment,
                        text=True, capture_output=True)
if result.returncode not in (0, 1):
    raise RuntimeError(result.stderr)
(args.output / 'results.jsonl').write_text(result.stdout)
export = 'objectives/exfiltration/stealer/env::native-detached-secret-env-json-http-export'
concealed = 'objectives/supply-chain/hidden-payload/native-extension::npm-concealed-native-env-export'
for line in result.stdout.splitlines():
    raw = json.loads(line)['raw']
    outer = raw['files'][0]
    hostile = {trait['id'] for trait in outer.get('traits', []) if trait['crit'] == 5}
    expected = {export, concealed} if Path(outer['path']) in paths[:2] else set()
    assert hostile == expected, (outer['path'], hostile, expected)
    print(Path(outer['path']).name, sorted(hostile))
