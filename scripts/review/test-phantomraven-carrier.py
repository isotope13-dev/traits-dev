#!/usr/bin/env python3
"""Distinguish a researched campaign host from a generic URL dependency."""
import io
import json
import pathlib
import subprocess
import tarfile
import tempfile

fixture = pathlib.Path('testdata/hostile/generated/npm-bad-20261028/noop-external-carrier.tgz')
with tarfile.open(fixture, 'r:gz') as source:
    entries = [(member.name, source.extractfile(member).read()) for member in source if member.isfile()]
with tempfile.TemporaryDirectory() as tmp:
    for name, old, new, expected in [
        ('known', b'packages.storeartifact.com', b'packages.storeartifact.com', True),
        ('other', b'packages.storeartifact.com', b'other-packages.invalid', False),
    ]:
        path = pathlib.Path(tmp) / (name + '.tgz')
        with tarfile.open(path, 'w:gz') as target:
            for entry, data in entries:
                data = data.replace(old, new)
                info = tarfile.TarInfo(entry)
                info.size = len(data)
                target.addfile(info, io.BytesIO(data))
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::phantomraven-storeartifact-noop-stage') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
        if name == 'other':
            assert not any(t['crit'] >= 5 for t in report['files'][0].get('traits', []))
print('PhantomRaven carrier boundaries passed.')
