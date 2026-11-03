#!/usr/bin/env python3
"""Chrome path fragment evidence must occur in one JavaScript array."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/path/application/browser/profile::chrome-profile-executable-fragments-array'
CASES = {
    'same-array': ("const a = ['User Data', 'Chrome', 'chrome.e'];", True),
    'escaped-space': ("const a = ['User\\x20Data', 'Chrome', 'chrome.e'];", True),
    'reordered': ('const a = ["chrome.e", "Chrome", "User Data"];', True),
    'two-arrays': ("const a=['Chrome', 'User Data']; const b=['chrome.e'];", False),
    'other-exe': ("const a=['Chrome', 'User Data', 'firefox.e'];", False),
    'missing-profile': ("const a=['Chrome', 'chrome.e'];", False),
    'comment': ("// ['Chrome', 'User Data', 'chrome.e']", False),
    'separate-strings': ("const a='Chrome', b='User Data', c='chrome.e';", False),
}
with tempfile.TemporaryDirectory(prefix='chrome-array-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(source + '\n')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        found = any(trait['id'] == RULE for trait in report.get('traits', []))
        assert found == CASES[name][1], (name, found, CASES[name][1])
print('Chrome profile and executable fragments require one array')
