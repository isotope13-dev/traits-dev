#!/usr/bin/env python3
"""Check shared matcher corrections on copied controls, outside testing suppressors."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

base = Path(__file__).resolve().parent
repo = base.parent.parent
cases = json.loads((base / 'cases.json').read_text())
# Require a caller-selected scratch root so artifacts stay in the review workspace.
with tempfile.TemporaryDirectory(prefix='package-behavior-', dir=sys.argv[1]) as tmp:
    root = Path(tmp)
    names = {}
    for name in cases:
        source = repo / cases[name]['source'] if 'source' in cases[name] else base / name
        if not source.exists():
            source = repo / 'testdata/js-tail-recursion' / name
        dest = root / ('METADATA' if name == 'license.METADATA' else name)
        shutil.copyfile(source, dest)
        names[str(dest)] = name
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(repo), SCAN_FOLLOW='none')
    proc = subprocess.run(
        ['atomscan', '--no-update', '--analyze', 'local', '--follow=none',
         '--mode', 'slow', '-f', 'json', *names],
        text=True, capture_output=True, env=env)
    (Path(sys.argv[1]) / 'controls.jsonl').write_text(proc.stdout)
    (Path(sys.argv[1]) / 'controls.log').write_text(proc.stderr)
    assert proc.returncode == 0, proc.stderr
    seen = set()
    for line in proc.stdout.split('\n'):
        if not line:
            continue
        report = json.loads(line)
        file = report['raw']['files'][0]
        name = names[file['path']]
        seen.add(name)
        ids = {f['id'] for f in file.get('traits', [])}
        for required in cases[name].get('required', []):
            assert required in ids, (name, 'missing', required)
        for forbidden in cases[name].get('forbidden', []):
            assert forbidden not in ids, (name, 'unexpected', forbidden)
        print(name, 'PASS', flush=True)
    assert seen == set(cases), ('unscanned', set(cases) - seen)
