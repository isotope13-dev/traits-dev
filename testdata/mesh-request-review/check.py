"""Check request-to-eval and path-versus-execution boundaries without execution."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
# Analyze copies outside testdata: existing path-based test suppressors otherwise
# suppress eval-call and prevent exercising the full webshell composite.
with tempfile.TemporaryDirectory(prefix='.mesh-request-review-', dir=root) as work:
    paths = []
    for case in cases:
        target = Path(work) / Path(case['path']).name
        shutil.copyfile(root / case['path'], target)
        paths.append(str(target))
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'jsonl', *paths],
        text=True, capture_output=True, check=True)
    assert not result.stderr.strip(), result.stderr
    observed = {}
    for line in result.stdout.splitlines():
        for item in json.loads(line)['files']:
            observed[Path(item['path']).name] = {t['id'] for t in item.get('traits', [])}
    for case in cases:
        actual = observed[Path(case['path']).name]
        missing = set(case.get('matched', [])) - actual
        unexpected = set(case.get('not_matched', [])) & actual
        assert not missing and not unexpected, (case['path'], missing, unexpected)
        print('PASS', case['path'])
