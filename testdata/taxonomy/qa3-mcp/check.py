#!/usr/bin/env python3
"""Focused severe-finding and rename checks; no specimen code is executed."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'objectives/supply-chain/trojanized/app/config-injection::'
INSTALL = PREFIX + 'npm-install-multi-client-mcp-registration'
NATIVE = PREFIX + 'multi-client-mcp-with-mutable-native-stage'
KILO = 'well-known/tool/development/agent/kilocode::'

def scan(path):
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', 'analyze', str(path)], check=True, capture_output=True, text=True)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    return [file for report in reports for file in report['files']]

def assert_suspicious(path):
    files = scan(path)
    root = files[0]
    severe = {t['id']: t['crit'] for t in root['traits'] if t['crit'] >= 4}
    assert severe == {INSTALL: 4, NATIVE: 4}, (path, severe)
    assert not any(t['id'].startswith(KILO) for file in files for t in file['traits']), path

archive = ROOT / 'testdata/purgatory/qa3-mcp-installer/hyperglob.tgz'
assert_suspicious(archive)
with tempfile.TemporaryDirectory(prefix='qa3-mcp-control-') as tmp:
    renamed = Path(tmp) / 'unrelated-package.tgz'
    with tarfile.open(archive, 'r:gz') as source, tarfile.open(renamed, 'w:gz') as target:
        for info in source:
            if not info.isfile():
                continue
            data = source.extractfile(info).read()
            if info.name.endswith(('.js', '.json')):
                data = data.replace(b'hyperglob', b'filelens').replace(b'Nom-nom-hub', b'other-owner')
            entry = tarfile.TarInfo(info.name)
            entry.size = len(data)
            target.addfile(entry, io.BytesIO(data))
    assert_suspicious(renamed)

for name in ['explicit-register.js', 'native-download.js', 'comment-only.js', 'kilo-bundle.js']:
    files = scan(ROOT / 'testdata/benign/qa3-mcp-controls' / name)
    severe = [t['id'] for file in files for t in file['traits'] if t['crit'] >= 4]
    assert not severe, (name, severe)
print('qa3 MCP: original, renamed package, and four benign controls passed')
