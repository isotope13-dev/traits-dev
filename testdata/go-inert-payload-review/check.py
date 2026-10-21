"""Exercise payload-content findings without test-path exclusions."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='go-payload-', dir=args.scratch) as directory:
    paths = []
    for index, case in enumerate(cases):
        path = Path(directory) / str(index) / 'module.go'
        path.parent.mkdir()
        path.write_bytes((root / case['path']).read_bytes())
        paths.append(path)
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                             *map(str, paths)], check=True, capture_output=True, text=True)
    reports = {}
    remaining = result.stdout
    decoder = json.JSONDecoder()
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report.get('files', []):
            reports[file['path']] = {trait['id'] for trait in file.get('traits', [])}
    for case, path in zip(cases, paths):
        ids = reports[str(path)]
        missing = set(case['matched']) - ids
        unexpected = set(case['not_matched']) & ids
        assert not missing and not unexpected, (case['path'], missing, unexpected)
        print('PASS', Path(case['path']).name)
