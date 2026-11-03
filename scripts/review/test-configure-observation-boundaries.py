#!/usr/bin/env python3
"""Distinguish shell configuration paths and tokens from HTTP/host clues."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
login = 'micro-behaviors/communications/http/login::http-login-path'
host = 'metadata/lang/source/syntax/directive::shell-host-directive-text'
cases = {
    'config.sh': ('#!/bin/sh\n[ "x$path" = "x/etc/default/login" ]\nhost\nbuild_os\n', set()),
    'route.sh': ('#!/bin/sh\nroute="/api/auth/login"\n', {login}),
    'host.sh': ('#!/bin/sh\nhost example.invalid\n', {host}),
}
with tempfile.TemporaryDirectory(prefix='configure-boundaries-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        f = json.loads(line)['files'][0]
        name = Path(f['path']).name
        actual = {t['id'] for t in f.get('traits', [])} & {login, host}
        assert actual == cases[name][1], (name, actual, cases[name][1])
        seen.add(name)
    assert seen == set(cases), seen
print('Configure path and host-token boundaries passed.')
