"""Scan static command construction fixtures; do not execute PowerShell."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
ids = {
    'objectives/credential-access/files/config::' + name
    for name in (
        'powershell-iis-apppool-password-command',
        'powershell-iis-vdir-password-command',
        'powershell-webconfig-connectionstrings-decrypt-command',
    )
}
paths = sorted(fixtures.glob('*.ps1'))
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json', *map(str, paths)],
    capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
seen = set()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        name = Path(file['path']).name
        if name not in {p.name for p in paths}:
            continue
        found = {t['id'] for t in file.get('traits', [])} & ids
        expected = ids if name == 'queries.ps1' else set()
        assert found == expected, (name, found, expected)
        seen.add(name)
assert seen == {p.name for p in paths}, seen
print('PASS: password queries, inventory, comments, and nearby names')
