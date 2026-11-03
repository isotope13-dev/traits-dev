#!/usr/bin/env python3
"""Check the GIF repeated-byte and truncated-extension observations."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
run = 'metadata/image/segment::gif-long-extension-byte-run'
combined = 'metadata/image/segment::gif-truncated-extension-with-long-run'
header = b'GIF89a\x01\x00\x01\x00\x00\x00\x00'
cases = {
    'broken.gif': (header + b'!' * 2048, {run, combined}),
    'short.gif': (header + b'!' * 100, set()),
    'valid.gif': (header + b'\x21\xfe\x05hello\x00;', set()),
}
with tempfile.TemporaryDirectory(prefix='gif-extension-run-') as tmp:
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
        actual = {t['id'] for t in file.get('traits', [])} & {run, combined}
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('GIF extension and byte-run boundaries passed.')
