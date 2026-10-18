"""Run controls outside testdata so fixture-path suppressors cannot mask findings."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--work-dir', required=True)
args = parser.parse_args()
base = Path(__file__).resolve().parent
root = base.parents[2]
cases = json.loads((base / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='launch-review-', dir=args.work_dir) as tmp:
    paths = []
    for case in cases:
        path = Path(tmp) / case['file']
        shutil.copyfile(base / case['file'], path)
        paths.append(str(path))
    run = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', *paths],
                         text=True, capture_output=True)
    if run.returncode:
        raise RuntimeError(run.stderr or run.stdout)
    decoder = json.JSONDecoder()
    text = run.stdout.strip()
    records = {}
    while text:
        report, end = decoder.raw_decode(text)
        records.update({Path(f['path']).name: f for f in report['files']})
        text = text[end:].lstrip()
    for case in cases:
        traits = records[case['file']]['traits']
        ids = {t['id'] for t in traits}
        assert set(case['present']) <= ids, (case['file'], 'missing', set(case['present']) - ids)
        assert not set(case['absent']) & ids, (case['file'], 'unexpected', set(case['absent']) & ids)
        assert not [t for t in traits if t['crit'] >= 4], (case['file'], 'unsupported intent')
print(f"PASS: {len(cases)} download/launch controls without fixture-path suppression")
