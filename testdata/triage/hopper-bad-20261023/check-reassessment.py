#!/usr/bin/env python3
"""Reassessment boundaries. Reads samples as data; never runs their code."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--inventory', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
p.add_argument('--output', required=True)
a = p.parse_args()
samples = json.loads(Path(a.inventory).read_text())['samples']

def sample(prefix):
    row = next(x for x in samples if x['sha256'].startswith(prefix))
    data = Path(row['local_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    return data

collector = 'objectives/credential-access/browser/multi-target::encrypted-native-multi-browser-collector'
loader = 'objectives/evasion/masquerade/version-resource/claim::fault-loader-conflicting-windows-identities'
npm = 'objectives/supply-chain/install-hook/proof-of-concept::concealed-install-temporary-package-command'
hid = 'objectives/evasion/security-bypass/policy/execution::hid-hidden-policy-bypass-eval'
cases = []
with tempfile.TemporaryDirectory(prefix='triage-reassessment-') as directory:
    directory = Path(directory)

    def add(name, data, yes=(), no=()):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, set(yes), set(no)))

    data = sample('993397')
    add('collector.exe', data, (collector,))
    needle = 'Google\\Chrome\\User Data'.encode('utf-16le')
    assert needle in data
    add('no-profile.exe', data.replace(needle, 'Google\\Chrome\\User Datz'.encode('utf-16le')), no=(collector,))
    pattern = rb'\xc7\x45.{5}\x4c\x8d\x45.\xc7\x45.{5}\x48\x8d\x55.\xc7\x45.{5}\x48\x8b\xd9'
    altered, count = re.subn(pattern, lambda m: b'\x90' + m[0][1:], data, flags=re.S)
    assert count >= 100, count
    add('no-dense-builders.exe', altered, no=(collector,))

    needle = bytes.fromhex('8b5424048b520cc602e983c2052bca894afc')
    for prefix in ['1f69b', '55a24', 'd9604']:
        data = sample(prefix)
        add(prefix + '.exe', data, (loader,))
        assert needle in data
        add(prefix + '-no-fault-patch.exe', data.replace(needle, b'\x90' + needle[1:]), no=(loader,))

    for prefix in ['76bd05', 'c3d0e6']:
        with tarfile.open(fileobj=io.BytesIO(sample(prefix)), mode='r:gz') as archive:
            member = next(x for x in archive.getmembers() if x.name.endswith('/package.json'))
            manifest = json.load(archive.extractfile(member))
        add(prefix + '/package.json', json.dumps(manifest), (npm,))
        hook = manifest['scripts']['postinstall']
        assert 'rm -rf $d' in hook
        manifest['scripts']['postinstall'] = hook.replace('rm -rf $d', 'echo complete')
        add(prefix + '-no-cleanup/package.json', json.dumps(manifest), no=(npm,))
    hook = 'd=$(mktemp -d); printf "{}" > $d/package.json; npm publish $d; rm -rf $d'
    add('visible-command/package.json', json.dumps({'name': 'control', 'version': '1.0.0', 'scripts': {'postinstall': hook}}), no=(npm,))

    for prefix, suffix in [('783e29', '.py'), ('d4cf79', '.txt')]:
        data = sample(prefix)
        add(prefix + suffix, data, (hid,))
        assert b'-WindowStyle Hidden' in data
        add(prefix + '-visible' + suffix, data.replace(b'-WindowStyle Hidden', b'-WindowStyle Normal'), no=(hid,))

    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd()))
    scan = subprocess.run([a.atomscan, '--no-update', '--mode', 'slow', '--format', 'json', 'path'] + [str(x[0]) for x in cases], env=env, capture_output=True, text=True)
    assert scan.returncode in (0, 1), scan.stderr
    found = {}
    for line in scan.stdout.splitlines():
        files = json.loads(line)['raw']['files']
        found[files[0]['path']] = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
    assert len(found) == len(cases), (len(found), len(cases), scan.stderr)
    result = []
    for path, yes, no in cases:
        traits = found[str(path)]
        assert all(traits.get(key) == 5 for key in yes), (path, yes, traits)
        assert not no.intersection(traits), (path, no.intersection(traits))
        result.append({'case': str(path.relative_to(directory)), 'required_hostile': sorted(yes), 'forbidden': sorted(no), 'passed': True})
    Path(a.output).write_text(json.dumps(result, indent=2) + '\n')
    print(f'{len(result)} reassessment boundary cases passed')
