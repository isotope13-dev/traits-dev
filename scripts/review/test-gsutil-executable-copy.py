#!/usr/bin/env python3
"""Check that the copy destination, not its source, is an executable path."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/file/copy/command::gsutil-copy-executable-path'
CASES = {
    'quoted': ('& \'gsutil\' -m cp "${latest}tool.exe" "C:\\tool.exe"', True),
    'unquoted': ('& \'gsutil\' -m cp "${latest}tool.exe" C:\\tool.exe', True),
    'plain': ('gsutil cp gs://bucket/tool C:\\tools\\helper.EXE', True),
    'other-destination': ('gsutil cp C:\\tool.exe C:\\other.txt', False),
    'remote-destination': ('gsutil cp C:\\tool.exe gs://bucket/tool.exe', False),
    'not-copy': ('gsutil ls C:\\tool.exe', False),
    'different-tool': ('other cp gs://bucket/tool C:\\tool.exe', False),
    'comment': ('# gsutil cp gs://bucket/tool C:\\tool.exe', False),
    'string': ('Write-Output "gsutil cp gs://bucket/tool C:\\tool.exe"', False),
}
with tempfile.TemporaryDirectory(prefix='gsutil-copy-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.ps1')
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
print('gsutil executable-copy observations identify the destination')
