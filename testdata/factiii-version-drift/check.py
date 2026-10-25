"""Scan static controls outside testdata so fixture-path exclusions cannot mask them."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parent
repo = root.parent.parent
cases = json.loads((root / 'cases.json').read_text())
env = os.environ.copy()
env['CLEAVE_TRAITS_DIR'] = str(repo)
with tempfile.TemporaryDirectory(prefix='factiii-controls-', dir=repo) as directory:
    paths = []
    for case in cases:
        target = Path(directory) / case['file']
        shutil.copyfile(root / case['file'], target)
        paths.append(str(target))
    result = subprocess.run(
        ['atomscan', '--no-update', '--analyze', 'local', '--mode', 'slow',
         '--follow=none', '-f', 'json', *paths], env=env, capture_output=True,
    )
    reports = [json.loads(line) for line in result.stdout.splitlines() if line]
    assert len(reports) == len(cases), result.stderr.decode(errors='replace')
    by_name = {Path(report['raw']['files'][0]['path']).name: report for report in reports}
    for case in cases:
        report = by_name[case['file']]
        traits = {trait['id']: trait['crit'] for file in report['raw']['files']
                  for trait in file.get('traits', [])}
        for trait in case.get('present', []):
            assert trait in traits, (case['file'], 'missing', trait)
        for trait in case.get('absent', []):
            assert trait not in traits, (case['file'], 'unwanted', trait)
        if case.get('neutral'):
            assert not any(crit >= 4 for crit in traits.values()), (case['file'], traits)
        print('PASS', case['file'])
