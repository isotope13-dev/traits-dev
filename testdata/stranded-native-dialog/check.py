"""Static controls; none of the AppleScript fixtures is executed."""
import argparse
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--sample', type=Path)
args = parser.parse_args()
base = Path(__file__).parent
rule = 'objectives/credential-access/phishing/lure::applescript-credential-phish-hostile'
cases = [(base / 'validated-dialog.applescript', True),
         (base / 'password-entry.applescript', False),
         (base / 'directory-auth.applescript', False),
         (base / 'pdf-password.applescript', False)]
if args.sample:
    cases.append((args.sample, True))
for path, expected in cases:
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), 'test-rules',
                             str(path), '--rules', rule],
                            text=True, capture_output=True, check=True)
    matched = any(line.startswith('MATCHED ' + rule + ' ')
                  for line in result.stdout.splitlines())
    assert matched == expected, (path, result.stdout, result.stderr)
    print(f'{path.name}: {"matched" if matched else "not matched"}')
