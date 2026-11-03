#!/usr/bin/env python3
"""A downloaded-file permission observation must bind both path expressions."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/chmod/executable/mode::curl-output-chmod-same-path'
CASES = {
    'same-path': ('curl --output /tmp/tool https://example.org/tool\nchmod +x /tmp/tool\n', True),
    'short-option': ('curl -o /tmp/tool https://example.org/tool\nchmod +x /tmp/tool\n', True),
    'quoted-url': ('curl -o /tmp/tool "https://example.org/tool"\nchmod +x /tmp/tool\n', True),
    'absolute-programs': ('/usr/bin/curl -o /tmp/tool https://example.org/tool\n/bin/chmod +x /tmp/tool\n', True),
    'variable-path': ('curl -o "$dst" https://example.org/tool\nchmod +x "$dst"\n', True),
    'function': ('stage() {\n curl -o /tmp/tool https://example.org/tool\n chmod +x /tmp/tool\n}\n', True),
    'and-list': ('curl -o /tmp/tool https://example.org/tool && chmod +x /tmp/tool\n', True),
    'different-path': ('curl -o /tmp/one https://example.org/tool\nchmod +x /tmp/two\n', False),
    'non-http': ('curl -o /tmp/tool ftp://example.org/tool\nchmod +x /tmp/tool\n', False),
    'read-only': ('curl -o /tmp/tool https://example.org/tool\nchmod 644 /tmp/tool\n', False),
    'comment': ('# curl -o /tmp/tool https://example.org/tool\nchmod +x /tmp/tool\n', False),
    'unrelated-delete': ('curl -o /tmp/tool https://example.org/tool\nchmod +x /tmp/tool\nrm -f /tmp/unrelated\n', True),
}
with tempfile.TemporaryDirectory(prefix='curl-chmod-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        p = Path(tmp) / (name + '.sh')
        p.write_text('#!/bin/sh\n' + source)
        paths.append(str(p))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for f in reports:
        name = Path(f['path']).stem
        got = any(t['id'] == RULE for t in f.get('traits', []))
        assert got == CASES[name][1], (name, got, CASES[name][1])
print('curl output and chmod target observations require the same path text')
