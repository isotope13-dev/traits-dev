#!/usr/bin/env python3
"""Check malformed JPEG comments separately from marker bytes in payloads."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
short = 'metadata/image/segment::jpeg-short-comment-length'
exploit = 'objectives/execution/exploit/buffer-overflow::jpeg-short-comment-with-nop-sled'
soi, eoi, nop = b'\xff\xd8', b'\xff\xd9', b'\x90' * 256
cases = {
    'malformed.jpg': (soi + b'\xff\xfe\x00\x01' + nop + eoi, {short, exploit}),
    'short-only.jpg': (soi + b'\xff\xfe\x00\x01' + b'\x00' * 256 + eoi, {short}),
    'valid-comment.jpg': (soi + b'\xff\xfe\x01\x02' + nop + eoi, set()),
    'marker-in-app.jpg': (soi + b'\xff\xe1\x00\x06\xff\xfe\x00\x01' + nop + eoi, set()),
}
with tempfile.TemporaryDirectory(prefix='jpeg-comment-') as tmp:
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
        actual = {t['id'] for t in file.get('traits', [])} & {short, exploit}
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('JPEG comment-length boundaries passed.')
