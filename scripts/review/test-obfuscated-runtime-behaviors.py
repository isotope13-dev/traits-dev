#!/usr/bin/env python3
"""Check sensitive operations with and without string-table obfuscation."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
prefix = 'objectives/anti-static/obfuscation/obfuscator/js-obfuscator::'
credential = prefix + 'obfuscated-credential-env-reference'
launch = prefix + 'obfuscated-computed-process-launch'
obfuscation = "const _0xabcd=[];_0xabcd['push'](_0xabcd['shift']());const chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';"
operations = 'const token=process.env.SERVICE_AUTH_TOKEN;spawn(program);'
cases = {'both.js': (obfuscation + operations, {credential, launch}), 'plain.js': (operations, set()), 'codec.js': (obfuscation, set())}
with tempfile.TemporaryDirectory(prefix='obfuscated-runtime-') as tmp:
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
        actual = {t['id'] for t in file.get('traits', [])} & {credential, launch}
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('Obfuscated runtime behavior boundaries passed.')
