"""Run CouchDB rewrite detection controls against the current traits tree."""
import json
import subprocess
from pathlib import Path

cases = json.loads(Path(__file__).with_name('cases.json').read_text())
for case in cases['fixtures']:
    rules = case['matched'] + case['not_matched']
    result = subprocess.run(
        ['cleave', '--traits-dir', '.', 'test-rules', '--rules', ','.join(rules), case['path']],
        capture_output=True, text=True, check=True,
    )
    output = result.stdout + result.stderr
    for rule in case['matched']:
        assert '\nMATCHED ' + rule + ' ' in output, output
    for rule in case['not_matched']:
        assert '\nNOT MATCHED ' + rule + ' ' in output, output
    print('PASS', case['path'], flush=True)
