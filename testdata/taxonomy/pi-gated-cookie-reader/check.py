"""Focused regression cases for the Pi gated-cookie-reader exception.

A Pi extension whose Chromium-cookie reader is opt-in gated (a
browserCookieAccess-style setting plus Pi manifest markers) must not convict
the session-hijack / postinstall-cookie-hijack hostile composites, even when
its reader uses renamed symbols and the archive declares a postinstall hook.
The same capability shape without the gate must still convict. No fixture
code is executed; cleave only scans the directory.
"""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
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
