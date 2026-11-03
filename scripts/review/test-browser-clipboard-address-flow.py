#!/usr/bin/env python3
"""Exercise the browser clipboard address-substitution flow and its boundaries."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/impact/crypto-manipulation/clipboard::browser-execcommand-clipboard-eth-substitution'
source = '''function scan() {
  document.execCommand('paste');
  var text = input.value;
  text = text.replace(/^(0x)[A-Fa-f0-9]{40}$/g, '0x1234567890abcdef1234567890abcdef12345678');
  input.value = text;
  document.execCommand('copy');
}
'''
cases = {
    'flow.js': (source, True),
    'unrelated-value.js': (source.replace('input.value = text;', 'input.value = other;'), False),
    'different-element.js': (source.replace('input.value = text;', 'other.value = text;'), False),
    'no-paste.js': (source.replace("document.execCommand('paste');", ''), False),
    'no-copy.js': (source.replace("document.execCommand('copy');", ''), False),
    'placeholder.js': (source.replace('1234567890abcdef1234567890abcdef12345678', '0000000000000000000000000000000000000000'), False),
    'comments.js': ('/*\n' + source + '\n*/\n', False),
}
with tempfile.TemporaryDirectory(prefix='clipboard-address-review-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    scan = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True)
    reports = [json.loads(line)['files'][0] for line in scan.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).name
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found)
print('Browser clipboard address-flow boundaries passed.')
