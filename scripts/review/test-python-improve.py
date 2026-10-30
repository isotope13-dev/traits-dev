#!/usr/bin/env python3
"""Check neutral reference findings and protected attack preservation statically."""
from concurrent.futures import ThreadPoolExecutor
import json
import lzma
import tempfile
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ENGINE = shlex.split(os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')))
TRAITS = Path(os.environ.get('TRAITS_DIR', ROOT))
CASES = json.loads((ROOT / 'scripts/review/python-improve-cases.json').read_text())['cases']
assert len(CASES) == 10


def check(case):
    path = ROOT / case['path']
    with tempfile.TemporaryDirectory(prefix='python-improve-') as directory:
        # Analyze endpoint-like paths; the fixture repository's directory name
        # must not supply a testing-context exception to the rules under test.
        target = Path(directory) / (path.stem if path.suffix == '.xz' else path.name)
        target.write_bytes(lzma.decompress(path.read_bytes()) if path.suffix == '.xz' else path.read_bytes())
        report = subprocess.run([*ENGINE, '--traits-dir', str(TRAITS), '--format', 'json', str(target)],
                                capture_output=True, text=True, check=True)
    files = json.loads(report.stdout)['files']
    all_ids = {trait['id'] for file in files for trait in file.get('traits', [])}
    assert set(case['required']) <= all_ids, (path.name, 'missing', set(case['required']) - all_ids)
    assert not set(case['forbidden']) & all_ids, (path.name, 'misleading', set(case['forbidden']) & all_ids)
    root_high = [trait for trait in files[0].get('traits', []) if trait.get('crit', 0) >= 4]
    hostile = {trait['id'].split('::')[0] for trait in root_high if trait['crit'] == 5}
    assert len(hostile) >= case['minimum_hostile'], (path.name, 'hostile coverage', hostile)
    if case['path'].startswith('testdata/notable/'):
        assert not root_high, (path.name, root_high)
    if case['path'].startswith('testdata/suspicious/'):
        assert root_high and not hostile, (path.name, root_high)
    if path.name.endswith('.zip'):
        recovered = [file for file in files if '.pyarmor-analysis.pyc' in file['path']]
        assert len(recovered) == 1, (path.name, 'missing recovered bytecode child')
    return path.name


with ThreadPoolExecutor(max_workers=3) as workers:
    passed = list(workers.map(check, CASES))
print(f'Python improvement regressions: {len(passed)} static fixtures passed')
