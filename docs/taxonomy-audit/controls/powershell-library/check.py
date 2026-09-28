"""Read-only rule traces; never execute the JavaScript controls.

Run from the traits repository: python3 docs/taxonomy-audit/controls/powershell-library/check.py
Optionally pass the cleave executable as the first argument.
"""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[4]
engine = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parent / 'cleave/target/release/cleave'
rule = 'well-known/lib/runtime/scripted/powershell-utils::powershell-utils-encoded-command-launcher'
expected = {'original': True, 'renamed-input': True, 'comments': False,
            'wrong-input': False, 'wrong-flags': False, 'wrong-launch': False}
for variant, matches in expected.items():
    sample = Path(__file__).resolve().parent / variant / 'node_modules/powershell-utils/index.js'
    result = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules',
                             '--rules', rule, str(sample)], text=True, capture_output=True, check=True)
    verdict = ('MATCHED ' if matches else 'NOT MATCHED ') + rule + ' (composite)'
    if not any(line.startswith(verdict) for line in result.stdout.splitlines()):
        raise AssertionError(f'{variant}: expected {verdict}\n{result.stdout}\n{result.stderr}')
    print(f'{variant}: expected verdict verified', flush=True)
