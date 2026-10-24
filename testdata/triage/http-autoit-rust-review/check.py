#!/usr/bin/env python3
"""Focused source/decoded-data and AutoIt behavioral controls."""
import json, os, subprocess
from pathlib import Path
base = Path(__file__).resolve().parent
cases = json.loads((base / 'cases.json').read_text())
cases += [
    (str(base.parents[1] / 'triage-streamlit-libraries/words.txt'), ['metadata/file/format/wordlist::one-token-per-line-list'], []),
    (str(base.parents[1] / 'taxonomy/stranded-shell-members/wildcard-field.json'), ['micro-behaviors/data/property/assign::wildcard-object-key'], []),
    (str(base.parents[1] / 'triage-streamlit-libraries/styles.css'), [], ['metadata/file/format/wordlist::one-token-per-line-list']),
]
env = dict(os.environ, CLEAVE_VALIDATE='0')
for name, positive, negative in cases:
    path = Path(name) if Path(name).is_absolute() else base / name
    result = subprocess.run(['cleave', 'test-rules', str(path), '--rules', ','.join(positive + negative)], env=env, text=True, capture_output=True, check=True)
    output = result.stdout + result.stderr
    for rule in positive:
        assert 'MATCHED ' + rule + ' ' in output, (name, rule, output)
    for rule in negative:
        assert 'NOT MATCHED ' + rule + ' ' in output, (name, rule, output)
    print('PASS', name)
