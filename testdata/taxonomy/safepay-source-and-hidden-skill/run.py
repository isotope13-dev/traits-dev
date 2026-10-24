#!/usr/bin/env python3
"""Exercise operation and intent boundaries using original fixture bytes."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--work-dir', required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='source-controls-', dir=args.work_dir) as staging:
    paths = []
    for number, case in enumerate(cases):
        source = repo / case['path']
        target = Path(staging) / str(number) / case.get('fixture_name', source.name)
        target.parent.mkdir()
        shutil.copyfile(source, target)
        paths.append(target)
    result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json',
                             *map(str, paths)], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    raw = result.stdout
    files = {}
    while raw.strip():
        report, end = decoder.raw_decode(raw.lstrip())
        raw = raw.lstrip()[end:]
        for file in report['files']:
            files[file['path']] = file
    for case, path in zip(cases, paths):
        file = files[str(path)]
        traits = {trait['id']: trait for trait in file.get('traits', [])}
        assert set(case['matched']) <= traits.keys(), (case['case_id'], 'missing', set(case['matched']) - traits.keys())
        assert not set(case['not_matched']) & traits.keys(), (case['case_id'], 'unexpected', set(case['not_matched']) & traits.keys())
        if case['case_id'] in ('own-token-thread.c', 'hidden-label.md', 'backup-transfer.bat'):
            assert not any(trait['crit'] == 5 for trait in traits.values()), (case['case_id'], 'unsupported hostile claim')
    print(f'PASS: {len(cases)} positive, negative, and retained-coverage controls')
