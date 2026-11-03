#!/usr/bin/env python3
"""Ensure API facts survive debugger paths without asserting remote targets."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='memory-taxonomy-') as tmp:
    root = Path(tmp)
    cases = {
        'neutral/fixture.py': 'kernel32.VirtualAllocEx(0, 0, 4096, 0x3000, 4)\nkernel32.WriteProcessMemory(0, 0, b"x", 1, 0)\n',
        'debugpy/fixture.py': 'kernel32.VirtualAllocEx(0, 0, 4096, 0x3000, 4)\nkernel32.WriteProcessMemory(0, 0, b"x", 1, 0)\n',
        'neutral/negative.py': 'kernel32.VirtualAllocEx(0, 0, 4096, 0x3000, 4)\n',
    }
    for name, source in cases.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {str(Path(r['path']).relative_to(root)): {t['id'] for t in r.get('traits', [])} for r in reports}
    evidence = 'micro-behaviors/mem/write/arbitrary::python-allocation-and-process-memory-write'
    assert set(ids) == set(cases), ids.keys()
    assert evidence in ids['neutral/fixture.py'] and evidence in ids['debugpy/fixture.py'], ids
    assert evidence not in ids['neutral/negative.py']
    print('Allocation/write evidence survives debugger paths and requires both calls.')
