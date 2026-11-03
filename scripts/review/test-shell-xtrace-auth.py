#!/usr/bin/env python3
"""Check tracing and variable authorization-header observations."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/communications/http/request/client::shell-xtrace-authorization-header'
source = '#!/bin/sh\nset -xeu\ncurl -H "Authorization: $token" "$url"\n'
cases = {
    'trace': (source, True),
    'option': (source.replace('set -xeu', 'set -o xtrace'), True),
    'braced': (source.replace('$token', '${token}'), True),
    'disabled': (source.replace('curl ', 'set +x\ncurl '), False),
    'disabled-option': (source.replace('curl ', 'set +o xtrace\ncurl '), False),
    'no-trace': (source.replace('-xeu', '-eu'), False),
    'comment': (source.replace('curl ', '# curl '), False),
    'literal-header': (source.replace('$token', 'placeholder'), False),
    'different-header': (source.replace('Authorization:', 'Accept:'), False),
}
with tempfile.TemporaryDirectory(prefix='shell-xtrace-auth-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.sh')
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, cases[name][1])
print('Shell tracing and authorization-header boundaries passed.')
