#!/usr/bin/env python3
"""Keep unrelated clues in a long minified line from forming a finding."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'metadata/file/profile/registry/access::powershell-registry-read-expression-clues'
prefix = r'Get-ItemProperty HKCU:\Software\Example; '
suffix = 'Invoke-Expression $payload'
cases = {'near.js': (prefix + suffix, True), 'far.js': (prefix + 'x' * 5000 + '; ' + suffix, False)}
with tempfile.TemporaryDirectory(prefix='registry-eval-proximity-') as tmp:
    paths = []
    for name, (text, _) in cases.items():
        path = Path(tmp) / name
        path.write_text('const command = ' + json.dumps(text) + ';\n')
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
print('Registry and expression proximity boundaries passed.')
