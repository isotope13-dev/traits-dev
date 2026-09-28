"""Read-only fetch/creation rule traces; no JavaScript is executed."""
from pathlib import Path
import subprocess
import sys
here = Path(__file__).resolve().parent
root = here.parents[3]
engine = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parent / 'cleave/target/release/cleave'
base = 'micro-behaviors/communications/http/services/github::'
rules = [base + 'github-contents-fetch-put', base + 'github-create-repo-and-contents-write']
positive = {'put', 'quoted-method', 'method-only', 'body-method-word'}
for sample in sorted(p for p in here.iterdir() if p.suffix in {'.js', '.ts'}):
    result = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules',
                             '--rules', ','.join(rules), str(sample)],
                            text=True, capture_output=True, check=True)
    for rule in rules:
        verdict = ('MATCHED ' if sample.stem in positive else 'NOT MATCHED ') + rule + ' ('
        if not any(line.startswith(verdict) for line in result.stdout.splitlines()):
            raise AssertionError(f'{sample.name}: expected {verdict}\n{result.stdout}\n{result.stderr}')
    print(f'{sample.name}: both expected verdicts verified', flush=True)
