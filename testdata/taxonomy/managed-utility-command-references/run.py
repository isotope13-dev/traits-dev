"""Check inert PE and PowerShell controls without executing their contents."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
case_file = Path(__file__).with_name('cases.json')
cases = json.loads(case_file.read_text())['fixtures']
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json',
     *[str(root / case['path']) for case in cases]],
    capture_output=True, text=True, check=True,
)
# Cleave can concatenate report documents for multiple inputs.
text = result.stdout.strip()
decoder = json.JSONDecoder()
observed = {}
while text:
    report, end = decoder.raw_decode(text)
    text = text[end:].lstrip()
    for file in report.get('files', []):
        observed[Path(file['path']).name] = {trait['id'] for trait in file['traits']}
for case in cases:
    actual = observed[Path(case['path']).name]
    missing = set(case['required_emitted']) - actual
    unexpected = set(case['forbidden_emitted']) & actual
    assert not missing and not unexpected, (case['case_id'], missing, unexpected)
print(f"PASS: {len(cases)} command-reference and placement controls")
