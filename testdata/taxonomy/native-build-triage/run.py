"""Run controls outside testdata, where scanner fixture suppressors apply."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
fixture_root = Path(__file__).resolve().parent
traits_root = fixture_root.parents[2]
cases = json.loads((fixture_root / 'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='native-build-controls-', dir=args.scratch) as work:
    control_root = Path(work)
    for case in cases:
        source = traits_root / case['path']
        relative = source.relative_to(fixture_root)
        destination = control_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(traits_root), '--format', 'jsonl', str(control_root)],
        text=True, capture_output=True, env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'},
    )
    if result.returncode:
        raise SystemExit(result.stderr)
    findings = {}
    for line in result.stdout.splitlines():
        for artifact in json.loads(line)['files']:
            findings[str(Path(artifact['path']).relative_to(control_root))] = {
                trait['id'] for trait in artifact.get('traits', [])
            }
    failures = []
    for case in cases:
        relative = str((traits_root / case['path']).relative_to(fixture_root))
        actual = findings.get(relative, set())
        for trait in case['matched']:
            if trait not in actual:
                failures.append(f'{relative}: missing {trait}')
        for trait in case['not_matched']:
            if trait in actual:
                failures.append(f'{relative}: unexpected {trait}')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'{len(cases)} native build and benign API controls passed')
