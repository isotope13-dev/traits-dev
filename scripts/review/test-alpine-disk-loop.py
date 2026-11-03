#!/usr/bin/env python3
"""Check the disk-write rule's loop bindings against mutated ELF copies."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
sample = Path(sys.argv[1])
source = sample.read_bytes()
loop = bytes.fromhex('48 89 45 f8 48 c7 45 f0 00 00 00 00 eb 15 48 8b 45 f8 48 89 c6 bf 61 00 00 00 e8 90 fe ff ff 48 ff 45 f0 b8 ff 27 6b ee 48 39 45 f0 7e e0')
offset = source.index(loop)
assert source.count(loop) == 1
changes = {'different-file': (17, b'\xf0'), 'different-counter': (34, b'\xf8'),
           'small-bound': (36, (100).to_bytes(4, 'little')), 'broken-back-edge': (45, b'\xdf')}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, (position, value) in changes.items():
        data = bytearray(source)
        data[offset + position:offset + position + len(value)] = value
        path = Path(directory) / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    for line in result.stdout.splitlines():
        report = json.loads(line)
        assert 'disk-fill-logic-bomb' not in json.dumps(report)
        assert 'x64-large-count-byte-write-loop' not in json.dumps(report)
    assert len(result.stdout.splitlines()) == len(paths)
print('Disk-write loop rejects changed handles, counters, bounds and back edges')
