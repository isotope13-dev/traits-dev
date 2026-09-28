"""Read-only classification checks; never execute the container examples."""
from pathlib import Path
import subprocess
import sys
here = Path(__file__).resolve().parent
root = here.parents[3]
engine = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parent / 'cleave/target/release/cleave'
rule = 'micro-behaviors/os/container/runtime::docker-privileged-spec'
for sample in sorted(p for p in here.iterdir() if p.suffix in {'.py', '.sh'} and p.name != 'check.py'):
    expected = sample.stem in {'hostconfig', 'nested-sibling', 'cli', 'cli-enabled'}
    result = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules',
                             '--rules', rule, str(sample)],
                            text=True, capture_output=True, check=True)
    verdict = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' ('
    if not any(line.startswith(verdict) for line in result.stdout.splitlines()):
        raise AssertionError(f'{sample.name}: expected {verdict}\n{result.stdout}\n{result.stderr}')
    print(f'{sample.name}: expected verdict verified', flush=True)
