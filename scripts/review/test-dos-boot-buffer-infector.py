#!/usr/bin/env python3
"""Require boot-buffer evidence beyond a disk-vector swap and file write."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/infect/binary/dos/interrupt::dos-resident-boot-buffer-infector'
VECTOR = bytes.fromhex('33 c0 8e d8 87 06 4c 00')
PATCH = bytes.fromhex('26 80 7f 4f ea 74 03 c7 07 eb 3c')
WRITE = bytes.fromhex('b8 01 03 33 db e8 28 00')
CALL = bytes.fromhex('9c 2e ff 1e 05 01 c3')
FILE_WRITE = bytes.fromhex('b4 40 cd 21')
cases = [
    ('infection_evidence', VECTOR + PATCH + WRITE + CALL, True),
    ('generic_vector_and_write', VECTOR + FILE_WRITE, False),
    ('no_vector', PATCH + WRITE + CALL, False),
    ('unknown_segment', bytes.fromhex('87 06 4c 00') + PATCH + WRITE + CALL, False),
    ('no_buffer_patch', VECTOR + WRITE + CALL, False),
    ('no_sector_write', VECTOR + PATCH + CALL, False),
    ('no_saved_call', VECTOR + PATCH + WRITE, False),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, payload, expected in cases:
        path = Path(tmp) / (name + '.com')
        path.write_bytes(payload.ljust(512, b'\x90'))
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE':'1'})
        findings = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
        found = any(t['id'] == RULE and t['crit'] == 5 for t in findings)
        assert found == expected, (name, found)
        if name == 'generic_vector_and_write':
            assert not any(t['crit'] == 5 for t in findings), [(t['id'], t['crit']) for t in findings]
print('DOS boot-buffer infection boundaries passed')
