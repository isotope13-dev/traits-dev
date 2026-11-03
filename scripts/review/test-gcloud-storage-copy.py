#!/usr/bin/env python3
"""Check cloud-copy recognition and source-text binding to chmod."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'micro-behaviors/fs/file/copy/command::'
CASES = {
    'same': ('gcloud storage cp "${src}/tool" tool\nchmod +x tool', (True, True)),
    'function': ('stage() {\n gcloud storage cp "$src" "$dst"\n chmod +x "$dst"\n}', (True, True)),
    'different': ('gcloud storage cp gs://bucket/a one\nchmod +x two', (True, False)),
    'upload': ('gcloud storage cp local gs://bucket/path', (True, False)),
    'other-mode': ('gcloud storage cp gs://bucket/a one\nchmod 644 one', (True, False)),
    'other-command': ('gcloud storage ls gs://bucket\nchmod +x tool', (False, False)),
    'comment': ('# gcloud storage cp gs://bucket/a one\nchmod +x one', (False, False)),
    'echo': ('echo gcloud storage cp gs://bucket/a one\nchmod +x one', (False, False)),
}
with tempfile.TemporaryDirectory(prefix='gcloud-copy-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.sh')
        path.write_text('#!/bin/sh\n' + source + '\n')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        ids = {trait['id'] for trait in report.get('traits', [])}
        found = (PREFIX + 'gcloud-storage-copy-command' in ids,
                 PREFIX + 'gcloud-copy-chmod-same-path' in ids)
        assert found == CASES[name][1], (name, found, CASES[name][1])
print('gcloud copy observations bind chmod to matching destination text')
