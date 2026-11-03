#!/usr/bin/env python3
"""Check that extension loading alone is not classified as a fork bomb."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
EXTENSION = 'metadata/import/module::gawk-fork-extension-load'
FORK = 'micro-behaviors/process/create/fork::awk-bare-fork-call'
BOMB = 'objectives/impact/dos/fork-bomb::gawk-fork-extension-endless-loop'
CASES = {
    'load-only.txt': '@load "fork"\nBEGIN { while (1) { print "tick" } }\n',
    'fork-loop.txt': '@load "fork"\nBEGIN { while (1) {\n  fork()\n} }\n',
}
with tempfile.TemporaryDirectory(prefix='fork-taxonomy-') as directory:
    paths = []
    for name, content in CASES.items():
        path = Path(directory) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', 'analyze', *paths], text=True, capture_output=True, check=True)
    found = {}
    for line in result.stdout.splitlines():
        for item in json.loads(line).get('files', []):
            found[Path(item['path']).name] = {trait['id'] for trait in item.get('traits', [])}
    assert EXTENSION in found['load-only.txt'], found
    assert FORK not in found['load-only.txt'] and BOMB not in found['load-only.txt'], found
    assert {EXTENSION, FORK, BOMB} <= found['fork-loop.txt'], found
print('Fork taxonomy: extension-only near miss and fork loop passed')
