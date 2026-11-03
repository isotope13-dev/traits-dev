#!/usr/bin/env python3
"""Check image terminator and hidden-iframe text boundaries."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
jpeg_trait = 'metadata/image/trailing::jpeg-end-remote-hidden-iframe'
gif_trait = 'metadata/image/trailing::gif-end-remote-hidden-iframe'
end = b'\xff\xd8\xff\xd9'
gif = b'GIF89a\x01\x00\x01\x00\x00\x00\x00;'
hidden = b'<iframe src=https://example.invalid/page height=0></iframe>'
visible = b'<iframe src=https://example.invalid/page height=100></iframe>'
cases = {
    'hidden.jpg': (end + hidden, {jpeg_trait}),
    'visible.jpg': (end + visible, set()),
    'before.jpg': (b'\xff\xd8' + hidden + b'\xff\xd9', set()),
    'hidden.gif': (gif + hidden + b' ' * 80, {gif_trait}),
    'visible.gif': (gif + visible + b' ' * 80, set()),
}
with tempfile.TemporaryDirectory(prefix='jpeg-iframe-') as tmp:
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
        actual = {t['id'] for t in file.get('traits', [])} & {jpeg_trait, gif_trait}
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('Image trailing iframe boundaries passed.')
