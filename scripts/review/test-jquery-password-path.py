#!/usr/bin/env python3
"""Recognize a password-labeled URL segment in a jQuery request."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/communications/http/request/credentials/application-state::jquery-getjson-password-path'
CASES = {
    'path': ("$.getJSON('https://example.test/password/'+encodeURIComponent(p)+'.json', cb);", True),
    'jquery': ('jQuery.getJSON("/password/" + encodeURIComponent(value), cb);', True),
    'other-path': ("$.getJSON('/username/'+encodeURIComponent(p), cb);", False),
    'other-call': ("other.getJSON('/password/'+encodeURIComponent(p), cb);", False),
    'not-url-argument': ("$.getJSON(url, '/password/'+encodeURIComponent(p));", False),
    'comment': ("// $.getJSON('/password/'+encodeURIComponent(p), cb);", False),
    'string': ('''console.log("$.getJSON('/password/'+encodeURIComponent(p))");''', False),
}
with tempfile.TemporaryDirectory(prefix='jquery-password-') as tmp:
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
print('jQuery password-path observation binds the first request argument')
