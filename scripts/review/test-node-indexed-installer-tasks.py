#!/usr/bin/env python3
"""Check independent clues in indexed download and Python tasking."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
changes = {
    'no-link-key': ('`link${i}`', '`item${i}`'),
    'no-python-key': ('`python${i}`', '`script${i}`'),
    'no-download-helper': ('downloadFile(', 'readLocalFile('),
    'no-http-post': ('axios.post(', 'axios.noop('),
    'no-process-exec': ('exec(', 'noop('),
    'no-silent-installer': ('/quiet', '/passive'),
    'no-polling': ('setInterval(', 'setTimeout('),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes):
        data = source
        if name in changes:
            old, new = changes[name]
            assert old in data, name
            data = data.replace(old, new)
        path = Path(directory) / (name + '.js')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::node-indexed-download-python-task-clues') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Indexed installer-task rule rejects seven missing-evidence controls')
