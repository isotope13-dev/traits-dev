#!/usr/bin/env python3
"""Test documented C2 and fake-error configuration evidence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/command-and-control/infrastructure/config::csharp-c2-config-fake-error'
SOURCE = '''class Config {
  // Display a fake error message at startup
  public static bool DisplayErrorMsg = true;
  // Hostname of C&C server
  public static string Server = "example.invalid";
}'''
cases = [
    ('configured', SOURCE, True),
    ('disabled', SOURCE.replace('= true', '= false'), False),
    ('no_fake_comment', SOURCE.replace('fake error', 'error'), False),
    ('no_c2_comment', SOURCE.replace('C&C server', 'server'), False),
    ('empty_server', SOURCE.replace('example.invalid', ''), False),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, source, expected in cases:
        path = Path(tmp) / (name + '.cs')
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('C# C2 and decoy configuration boundaries passed')
