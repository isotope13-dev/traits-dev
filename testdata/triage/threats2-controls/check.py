"""Check attack controls and nearby benign cases without test-path suppression."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='t2check-', dir='/tmp') as work:
    paths = []
    for case in cases:
        path = Path(work) / Path(case['path']).name
        shutil.copyfile(repo / case['path'], path)
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         '--format', 'json', *paths],
        env=dict(os.environ, CLEAVE_SKIP_CACHE='1'),
        capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    text = result.stdout
    pos = 0
    actual = {}
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos == len(text):
            break
        report, pos = decoder.raw_decode(text, pos)
        for file in report['files']:
            actual[Path(file['path']).name] = {
                trait['id'] for trait in file.get('traits', [])
            }
    failures = []
    for case in cases:
        name = Path(case['path']).name
        found = actual.get(name, set())
        missing = set(case['matched']) - found
        unexpected = set(case['not_matched']) & found
        failed = missing or unexpected or name not in actual
        print(name, 'FAIL' if failed else 'PASS', flush=True)
        if failed:
            failures.append({'file': name, 'missing': sorted(missing),
                             'unexpected': sorted(unexpected),
                             'analyzed': name in actual})
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
