#!/usr/bin/env python3
"""Check the YAML download-to-shell command-text boundary."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/process/deploy/interpreter-stdin::yaml-curl-pipe-shell-text'
cases = {
    'command.yml': ('steps:\n  - run: |\n      curl -o- -L https://example.invalid/install.sh | bash\n', True),
    'list.yml': ('commands:\n  - curl -fsSL https://example.invalid/install.sh | sh\n', True),
    'comment.yml': ('steps:\n  # curl -fsSL https://example.invalid/install.sh | sh\n', False),
    'separate.yml': ('steps:\n  - curl -o tool https://example.invalid/tool\n  - sh tool\n', False),
}
with tempfile.TemporaryDirectory(prefix='yaml-curl-shell-') as tmp:
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
print('YAML curl-to-shell command-text boundaries passed.')
