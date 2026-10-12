"""Focused regression cases for minecraftaccfinder triage traits.

Covers the urllib positional-body atom and the Python Discord-webhook
credential-exfil hostile. No fixture code is executed; cleave only scans
the directory.

Note on harness suppression: files under testdata/ match the test-directory
component, so the hostile (which carries a testing-harness `unless:`) cannot
fire on the loose discord-notify.py fixture — only its legs are asserted
there. The positive case runs through the wheel member path
(discord-cred-exfil-fixture.whl!!credhook/__init__.py): inner archive paths
do not carry the testdata/ prefix, so the file-scope composite fires there.
The hostile's archive-scope positive is the real minecraftaccfinder 3.0.0
sample, verified via `atomscan <path>`.
"""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json',
     str(Path(__file__).parent)],
    cwd=root, capture_output=True, text=True, check=True,
)
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
files = {}
while remaining:
    report, consumed = decoder.raw_decode(remaining)
    remaining = remaining[consumed:].lstrip()
    for entry in report['files']:
        path = Path(entry['path'])
        if path.is_absolute():
            path = path.relative_to(root)
        files[str(path)] = {trait['id'] for trait in entry.get('traits', [])}
checks = 0
for case in cases:
    actual = files[case['path']]
    for expected, present in [('matched', True), ('not_matched', False)]:
        for trait in case[expected]:
            assert (trait in actual) == present, (case['path'], expected, trait)
            checks += 1
print(f'{checks} trait assertions passed')
