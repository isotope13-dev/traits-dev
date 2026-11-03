#!/usr/bin/env python3
"""Check the combined array-rotation and computed-constructor observation."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/anti-static/obfuscation/string/reconstruct/transformation::computed-constructor-with-rotated-conditional-index'
rotation = 'items.unshift(items.pop()); function get(i){return items[i>0x37?i-0x38:i+0x1b];}'
constructor = 'new (obj["constructor"])("return x")(require);'
cases = {'both.js': (rotation + constructor, True), 'rotation.js': (rotation, False), 'constructor.js': (constructor, False)}
with tempfile.TemporaryDirectory(prefix='rotated-indexed-js-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(source)
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
print('Rotated and indexed JavaScript boundaries passed.')
