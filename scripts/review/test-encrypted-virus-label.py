#!/usr/bin/env python3
"""An archive's member name cannot prove the contents are hostile."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'well-known/malware/virus/archive-label::encrypted-labeled-virus-archive'
BADJOKE = 'metadata/archive/encryption::encrypted-badjoke-labeled-member'
with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp)
    sample = directory / 'Virus.DOS.Demo'
    sample.write_text('This is harmless sample text.\n')
    for password in ('unlikely-test-password-64e0', 'infected'):
        archive = directory / ('sample-' + password + '.7z')
        subprocess.run(['7z', 'a', '-t7z', '-p' + password, str(archive), sample.name],
                       cwd=directory, check=True, stdout=subprocess.DEVNULL)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(archive)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        files = json.loads(result.stdout)['files']
        findings = [t for f in files for t in f.get('traits', [])]
        assert any(t['id'] == RULE and t['crit'] == 4 for t in findings), password
        assert not any(t['crit'] == 5 for t in findings), password
    sample = directory / 'not-virus_BadJoke.Win32.Demo.exe'
    sample.write_text('This is harmless sample text.\n')
    archive = directory / 'badjoke.7z'
    subprocess.run(['7z', 'a', '-t7z', '-pinfected', str(archive), sample.name],
                   cwd=directory, check=True, stdout=subprocess.DEVNULL)
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(archive)],
                            check=True, capture_output=True, text=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    findings = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    assert any(t['id'] == BADJOKE and t['crit'] == 3 for t in findings)
    assert not any(t['id'] == RULE or t['crit'] >= 4 for t in findings)
print('Encrypted AV-style member names do not establish hostility')
