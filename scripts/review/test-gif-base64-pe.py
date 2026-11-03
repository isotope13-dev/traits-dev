#!/usr/bin/env python3
"""Check a GIF parse problem plus a PE-like Base64 prefix."""
import base64
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'metadata/image/trailing::gif-structure-problem-with-base64-pe-prefix'
header = b'GIF89a\x01\x00\x01\x00\x00\x00\x00'
payload = base64.b64encode(b'MZ\x90\x00\x03\x00' + bytes(range(128)))
cases = {
    'broken.gif': (header + b'\x21\x21\xff' + payload, True),
    'comment.gif': (header + b'\x21\xfe' + bytes([len(payload)]) + payload + b'\x00;', False),
    'no-pe.gif': (header + b'\x21\x21\xff' + b'A' * len(payload), False),
}
with tempfile.TemporaryDirectory(prefix='gif-base64-pe-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_bytes(source)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        file = json.loads(line)['files'][0]
        name = Path(file['path']).name
        actual = any(t['id'] == trait for t in file.get('traits', []))
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('GIF Base64 PE-like prefix boundaries passed.')
