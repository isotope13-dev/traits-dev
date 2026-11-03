#!/usr/bin/env python3
"""Check that screenshot reporting and download execution clues are required."""
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
    'no-screen': ('desktopCapturer.getSources', 'desktopCapturer.notSources'),
    'no-report': ('/screenshot', '/redacted'),
    'no-task-files': ('session.dataFiles', 'session.noFiles'),
    'no-task-apps': ('session.applications', 'session.noApps'),
    'no-download': ('downloadFileFromURL', 'removedDownload'),
    'no-elevation': ('-Verb RunAs', '-Verb None'),
    'no-detach': ('detached: true', 'detached: false'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes):
        data = source
        if name in changes:
            before, after = changes[name]
            assert before in data
            data = data.replace(before, after)
        path = Path(directory) / (name + '.js')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::electron-screenshot-tasked-download-execution')
                    for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Electron screenshot download task rejects seven controls')
