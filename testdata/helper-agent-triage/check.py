"""Focused regression cases for helper-agent triage traits.

Covers the dynamic FLAG env lookup atom and the https.request OOB beacon
composites. No fixture code is executed; cleave only scans the directory.

Note on harness suppression: files under testdata/ match the test-directory
component, so composites carrying a testing-harness `unless:` cannot fire on
the loose fixtures here. That is why:
- js-https-post-oob is asserted on the tgz member path (inner paths do not
  carry the testdata/ prefix, so the file-scope composite fires there), and
- npm-postinstall-oob-https-beacon (archive scope, sees the outer testdata/
  path) is asserted as not_matched here; its positive case is the real
  helper-agent 1.0.4 sample, verified via `atomscan <path>`.
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
