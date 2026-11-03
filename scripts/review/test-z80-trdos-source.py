#!/usr/bin/env python3
"""Check the TR-DOS source pattern with independent synthetic assembly."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/infect/binary/asm-source::z80-trdos-basic-entry-copy-source'
SOURCE = """\
        RST 56
        EXX
        DEC SP
        DEC SP
        POP AF
        EX AF,AF'
        LD C,5
        CALL #3D13
        CP "B"
        JR NZ,FIND
        ADD A,SIZE
        LD (HL),A
        EX AF,AF'
        PUSH AF
        POP HL
        DEC HL
        LDIR
        LD C,6
        CALL #3D13
"""

def matches(source):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'fixture.txt'
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))

assert matches(SOURCE)
assert matches(SOURCE.replace('\n', '\r\n').lower())
for old, new in [('LD C,5', 'LD C,4'), ('LD C,6', 'LD C,7'),
                 ('CP "B"', 'CP "C"'), ('LD (HL),A', 'LD (DE),A'),
                 ('RST 56', 'RST 48'), ('POP AF', '; POP AF'),
                 ('PUSH AF', '; PUSH AF'), ('LDIR', '; LDIR')]:
    assert not matches(SOURCE.replace(old, new)), old
assert not matches('\n'.join('; ' + line for line in SOURCE.splitlines()))
print('TR-DOS source finding requires each code observation and ignores comment-only examples')
