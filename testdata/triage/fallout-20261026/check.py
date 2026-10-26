#!/usr/bin/env python3
"""Static regression checks: no sample code, credentials or network executes."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CLEAVE = os.environ.get('CLEAVE', 'cleave')
CHAIN = 'objectives/exfiltration/stealer/credential::node-auth-files-encrypted-zip-upload'
EXPORT = 'objectives/exfiltration/stealer/credential::cross-agent-auth-encrypted-zip-upload'
FAMILY = 'well-known/malware/stealer/aokigahara::credential-archive-upload'
GATE = 'micro-behaviors/crypto/verify::powershell-computehash-digest-comparison'


def scan(paths):
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json',
                             *map(str, paths)], check=True, capture_output=True,
                            text=True, env={**os.environ, 'CLEAVE_VALIDATE': '0'})
    decoder, text, files = json.JSONDecoder(), result.stdout, []
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        files.extend(report['files'])
    return {Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])}
            for f in files}


observed = scan(sorted(HERE.glob('*.js')) + sorted(HERE.glob('*.ps1')) + sorted(
    (ROOT / 'testdata/powershell-hash-gated-loader').glob('*.ps1')))
for name in ('encrypted-agent-upload.js', 'renamed-locals.js'):
    assert observed[name][CHAIN] == 4, name
    assert observed[name][EXPORT] == 5, name
    assert observed[name][FAMILY] == 5, name
for name in ('archive-not-sent.js', 'archive-overwritten.js',
             'read-map-not-zipped.js', 'cipher-not-used.js',
             'ordinary-backup.js', 'catalog-no-read.js', 'ordinary-upload.js'):
    assert not ({CHAIN, EXPORT, FAMILY} & observed[name].keys()), name
for name in ('gated_loader.ps1', 'hash_verify_only.ps1'):
    assert observed[name][GATE] == 3, name
assert not any(c == 5 for c in observed['gated_loader.ps1'].values())
assert not any(c == 5 for c in observed['protected-hello.ps1'].values())
assert GATE not in observed['config_decrypt.ps1']
print('PASS: positive, renamed-local, broken-flow, benign and digest controls')
