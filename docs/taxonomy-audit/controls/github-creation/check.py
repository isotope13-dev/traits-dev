"""Check creation claims without executing any JavaScript control."""
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[3]
engine = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parent / 'cleave/target/release/cleave'
rule = 'micro-behaviors/communications/http/services/github::github-create-repo'
cases = {'path-only': False, 'get-route': False, 'fields-only': False,
         'post-route': True, 'octokit': True, 'org-call': True, 'helper-post': False}
for name, expected in cases.items():
    result = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules',
                             '--rules', rule, str(here / (name + '.js'))],
                            text=True, capture_output=True, check=True)
    verdict = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' (composite)'
    if not any(line.startswith(verdict) for line in result.stdout.splitlines()):
        raise AssertionError(f'{name}: expected {verdict}\n{result.stdout}\n{result.stderr}')
    print(f'{name}: expected verdict verified', flush=True)
