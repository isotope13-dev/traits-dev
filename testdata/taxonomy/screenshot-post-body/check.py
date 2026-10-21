"""Check screenshot body flow controls; optionally reuse a saved Cleave report."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', type=Path)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
case_file = Path(__file__).with_name('cases.json')
cases = json.loads(case_file.read_text())['fixtures']
if args.report:
    output = args.report.read_text()
else:
    output = subprocess.check_output(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         '--format', 'json', *[case['path'] for case in cases]],
        cwd=repo, text=True,
    )
reports = {}
decoder = json.JSONDecoder()
while output.strip():
    document, end = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[end:]
    for file in document['files']:
        reports[Path(file['path']).name] = file
for case in cases:
    report = reports[Path(case['path']).name]
    traits = {trait['id']: trait for trait in report.get('traits', [])}
    for trait in case['matched']:
        assert trait in traits, (case['path'], 'missing', trait)
        assert traits[trait]['crit'] == 3, (case['path'], 'must remain notable')
    for trait in case['not_matched']:
        assert trait not in traits, (case['path'], 'unexpected', trait)
print(f"Passed {len(cases)} screenshot POST body controls")
