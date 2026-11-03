#!/usr/bin/env python3
"""An unused fork result must not suppress an unbounded fork loop."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
BOMB = 'objectives/impact/dos/fork-bomb::unreaped-process-spawn-bomb'
ASSIGN = 'micro-behaviors/process/create/fork::python-fork-return-assignment'
BRANCH = 'micro-behaviors/process/create/fork::python-fork-child-zero-test'
CASES = {
    'unused.py': 'import os\npid = os.fork()\nwhile True: os.fork()\n',
    'branched.py': 'import os\npid = os.fork()\nif pid == 0:\n    print("child")\nwhile True: os.fork()\n',
}
with tempfile.TemporaryDirectory(prefix='fork-handling-') as directory:
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
    assert {ASSIGN, BOMB} <= found['unused.py'], found
    assert {ASSIGN, BRANCH} <= found['branched.py'] and BOMB not in found['branched.py'], found
print('Fork handling: unused assignment and child-branch cases passed')
