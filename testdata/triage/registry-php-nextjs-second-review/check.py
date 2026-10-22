"""Check Flight gadget admission and neutral Metasploit scaffolding."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
if args.report:
    output = args.report.read_text()
else:
    output = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--all-files', '--format', 'json',
         *[case['path'] for case in cases]],
        cwd=root, text=True, capture_output=True, check=True,
    ).stdout
files = {}
decoder = json.JSONDecoder()
while output.strip():
    output = output.lstrip()
    document, end = decoder.raw_decode(output)
    output = output[end:]
    for item in document['files']:
        files[Path(item['path']).name] = item
for case in cases:
    item = files[Path(case['path']).name]
    traits = {trait['id']: trait['crit'] for trait in item['traits']}
    missing = set(case['matched']) - traits.keys()
    extra = set(case['not_matched']) & traits.keys()
    assert not missing and not extra, (case['path'], missing, extra)
    if 'max_hostile' in case:
        assert sum(level == 5 for level in traits.values()) <= case['max_hostile'], case['path']
print(f'{len(cases)} focused regression cases passed')
