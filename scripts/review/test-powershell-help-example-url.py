#!/usr/bin/env python3
"""A help-example URL observation must not cross the end of a help block."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'metadata/package/documentation/powershell-help::powershell-example-url-context'
cases = {
    'within-example': ('<#\n.EXAMPLE\nGet-Thing https://example.org/a\n#>\n', True),
    'crlf': ('<#\r\n.EXAMPLE\r\nGet-Thing https://example.org/a\r\n#>\r\n', True),
    'outside-block': ('<#\n.EXAMPLE\nGet-Thing\n#>\n$url="https://example.org/a"\n', False),
    'preceding-url': ('$url="https://example.org/a"\n<#\n.EXAMPLE\nGet-Thing\n#>\n', False),
    'different-directive': ('<#\n.DESCRIPTION\nhttps://example.org/a\n#>\n', False),
}
with tempfile.TemporaryDirectory(prefix='help-url-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / (name + '.ps1')
        # Ordinary scans apply a small-file floor to this notable trait.
        # Add neutral material after the tested block so the fixture exercises
        # the matcher rather than that unrelated floor.
        path.write_text(source + ('# padding\n' * 30) + 'function Get-Thing { return 1 }\n', newline='')
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                            check=True, capture_output=True, text=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for f in reports:
        name = Path(f['path']).stem
        got = any(t['id'] == RULE for t in f.get('traits', []))
        assert got == cases[name][1], (name, got, cases[name][1])
print('Help-example URL observation does not cross the block terminator')
