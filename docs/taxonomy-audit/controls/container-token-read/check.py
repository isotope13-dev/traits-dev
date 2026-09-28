"""Check classification by scanning examples; never execute their contents."""
from pathlib import Path
import subprocess
import sys
here = Path(__file__).resolve().parent
root = here.parents[3]
engine = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parent / 'cleave/target/release/cleave'
rules = ['metadata/file/string/file::token-read-text-reference',
         'micro-behaviors/os/container/runtime::incluster-apply-client']
for sample in sorted(p for p in here.glob('*.py') if p.name != 'check.py'):
    expected = [sample.stem in {'local', 'method-reference', 'cluster'}, sample.stem == 'cluster']
    result = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules',
                             '--rules', ','.join(rules), str(sample)],
                            text=True, capture_output=True, check=True)
    for rule, match in zip(rules, expected):
        verdict = ('MATCHED ' if match else 'NOT MATCHED ') + rule + ' ('
        assert any(line.startswith(verdict) for line in result.stdout.splitlines()), result.stdout + result.stderr
    print(f'{sample.name}: both expected verdicts verified', flush=True)
