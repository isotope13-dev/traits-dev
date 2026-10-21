"""Run the semantic controls with neutral paths (buffer rules exclude tests)."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads((Path(__file__).parent / 'cases.json').read_text())['fixtures']
control_dir = Path(args.scratch).resolve()
control_dir.mkdir(parents=True, exist_ok=True)
for case in cases:
    source = root / case['path']
    target = control_dir / source.name
    shutil.copyfile(source, target)
    if 'pad_to_bytes' in case:
        text = target.read_text()
        target.write_text(text + '/*' + '.' * (case['pad_to_bytes'] - len(text) - 4) + '*/\n')
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json', str(control_dir)],
    check=True, text=True, stdout=subprocess.PIPE,
)
(control_dir.parent / "control-scan.json").write_text(result.stdout)
remaining = result.stdout
files = {}
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        files[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
for case in cases:
    actual = files[Path(case['path']).name]
    missing = set(case['matched']) - actual
    extra = set(case['not_matched']) & actual
    assert not missing and not extra, (case['case_id'], missing, extra)
    print('PASS', case['case_id'])
print(f'{len(cases)} controls passed')
