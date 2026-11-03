#!/usr/bin/env python3
"""Generic BIOS disk operations do not prove destructive wiping."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
CASES = [
    ('fixed', 'b80103ba8000cd13b44ccd21', 'dos-fixed-disk-write-and-exit'),
    ('copy', 'b80202cd137200b80203cd13b44ccd21', 'dos-raw-sector-copy-and-exit'),
    ('boot', 'b80103bb007cb9010031d2cd13b8004ccd21', 'dos-boot-sector-write-and-exit'),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, hexadecimal, trait in CASES:
        path = Path(tmp) / (name + '.com')
        path.write_bytes(bytes.fromhex(hexadecimal).ljust(512, b'\x90'))
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        findings = [t for f in json.loads(proc.stdout)['files'] for t in f.get('traits', [])]
        assert any(t['id'].endswith('::' + trait) and t['crit'] == 3 for t in findings), (name, [(t['id'],t['crit']) for t in findings])
        assert not any(t['crit'] == 5 for t in findings), (name, [(t['id'],t['crit']) for t in findings if t['crit'] == 5])
print('Raw disk observations do not alone establish wiping')
