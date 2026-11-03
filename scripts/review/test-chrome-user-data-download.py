#!/usr/bin/env python3
"""A response stream must use the constructed Chrome-profile destination."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'micro-behaviors/fs/path/application/browser/profile::'
SOURCE = '''
async function stage(url) {
  return new Promise((resolve, reject) => {
    const file = "chrome.e" + "xe", dir = path["join"](os["homedir"](), "AppData", "Local", "Google", "Chrome", "User Data"), dest = path['join'](dir, file);
    const client = url.startsWith('https:') ? https : http;
    client['get'](url, response => {
      const stream = fs['createWriteStream'](dest);
      response['pipe'](stream), stream.on('finish', () => resolve(dest));
    })['on']('error', reject);
  });
}
'''
CASES = {
    'complete': (SOURCE, True, True),
    'different-write': (SOURCE.replace("createWriteStream'](dest)", "createWriteStream'](other)"), True, False),
    'different-response': (SOURCE.replace("response['pipe']", "other['pipe']"), True, False),
    'different-stream': (SOURCE.replace("['pipe'](stream)", "['pipe'](other)"), True, False),
    'different-client': (SOURCE.replace("client['get']", "other['get']"), True, False),
    'different-filename': (SOURCE.replace('dest = path[\'join\'](dir, file)', 'dest = path[\'join\'](dir, other)'), False, False),
    'different-directory': (SOURCE.replace('"User Data"', '"Other Data"'), False, False),
    'comment': ('/* ' + SOURCE + ' */', False, False),
}
with tempfile.TemporaryDirectory(prefix='chrome-download-') as tmp:
    paths = []
    for name, (source, _, _) in CASES.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(source)
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        ids = {trait['id'] for trait in report.get('traits', [])}
        found = (PREFIX + 'chrome-user-data-executable-path' in ids,
                 PREFIX + 'chrome-user-data-download-stream' in ids)
        assert found == CASES[name][1:], (name, found, CASES[name][1:])
print('Chrome-profile download observation binds destination and stream')
