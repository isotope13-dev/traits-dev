#!/usr/bin/env python3
"""Check backward jumps, forward jumps and bare labels against loop traits."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
ORDERED = 'micro-behaviors/data/control-flow/loop/unconditional::batch-loop-label-before-jump'
AWK = 'micro-behaviors/data/control-flow/loop/unconditional::awk-begin-infinite-loop'
CASES = {
    'backward.bat': ':loop\necho tick\ngoto loop\n',
    'forward.bat': 'goto loop\necho tick\n:loop\n',
    'label.bat': ':loop\necho tick\n',
    'busy.txt': 'BEGIN { while (1) { print "tick" } }\n',
}
with tempfile.TemporaryDirectory(prefix='control-flow-boundaries-') as temporary:
    paths = []
    for name, text in CASES.items():
        path = Path(temporary) / name
        path.write_text(text)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', 'analyze', *paths], text=True, capture_output=True, check=True)
    found = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line).get('files', []):
            found[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
    assert ORDERED in found['backward.bat'], found
    assert ORDERED not in found['forward.bat'], found
    assert not any(trait.startswith('micro-behaviors/data/control-flow/loop/') for trait in found['label.bat']), found
    assert AWK in found['busy.txt'], found
print('Control-flow boundaries: backward edge, forward edge, bare label and AWK loop passed')
