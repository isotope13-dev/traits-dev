"""Focused controls for the PixelFormat and RAR-shape false positives."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
engine = os.environ.get('CLEAVE', 'cleave')
for case in cases['fixtures']:
    rules = case.get('matched', []) + case.get('not_matched', [])
    command = [engine, '--traits-dir', str(root)]
    trace = subprocess.run(command + ['test-rules', str(root / case['path']),
                                     '--rules', ','.join(rules)],
                           check=True, capture_output=True, text=True).stdout
    for trait in case.get('matched', []):
        assert any(line.startswith('MATCHED ' + trait + ' ') for line in trace.splitlines()), (case['case_id'], trait, trace)
    for trait in case.get('not_matched', []):
        assert any(line.startswith('NOT MATCHED ' + trait + ' ') for line in trace.splitlines()), (case['case_id'], trait, trace)
    report = json.loads(subprocess.run(command + ['--format', 'json', str(root / case['path'])],
                                      check=True, capture_output=True, text=True).stdout)
    for file in report['files']:
        for trait in file['traits']:
            assert trait['crit'] < 4, (case['case_id'], trait)
            assert trait['id'] not in case['forbidden_emitted'], (case['case_id'], trait)
    print('PASS', case['case_id'], flush=True)
