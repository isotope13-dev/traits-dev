"""Check inert native controls and the existing Braintree theft specimen.

No fixture is executed. Binary controls distinguish reference context and
exercise the retained attack composites; they do not claim runnable behavior.
"""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENGINE = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
CASES = json.loads((HERE / 'cases.json').read_text())

def reports(path):
    result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json',
                             str(path)], capture_output=True, text=True, check=True)
    text = result.stdout.strip()
    decoder = json.JSONDecoder()
    while text:
        value, end = decoder.raw_decode(text)
        yield from value['files']
        text = text[end:].strip()

for case in CASES:
    actual = {t['id'] for f in reports(ROOT / case['path']) for t in f.get('traits', [])}
    assert set(case['present']) <= actual, (case['path'], set(case['present']) - actual)
    assert not set(case['absent']) & actual, (case['path'], set(case['absent']) & actual)
print(f'PASS: {len(CASES)} native context/attack controls and Braintree theft fixture')
