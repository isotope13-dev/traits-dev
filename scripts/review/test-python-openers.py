#!/usr/bin/env python3
"""Check Python opener calls and nearby non-call references."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULES = ','.join('micro-behaviors/process/create/shellexec::' + rule for rule in
                 ('os-startfile-call', 'webbrowser-open'))

cases = (
    ('calls', 'import os\nimport webbrowser\nos.startfile("app.exe")\n'
              'webbrowser.open_new_tab("https://example.org")\n', 2),
    ('references', 'import webbrowser\nhandler = webbrowser.open\n'
                   'other.startfile("file")\n', 0),
    ('bare-import', 'from os import startfile\nstartfile("app.exe")\n', 1),
)
with tempfile.TemporaryDirectory(prefix='python-openers-') as temp:
    for name, source, expected in cases:
        path = Path(temp) / (name + '.py')
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', RULES, str(path)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        summary = f'Summary: {expected} matched, {2 - expected} not matched'
        if summary not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
