"""Static matcher regressions; fixture code is never executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).parent
CASES = json.loads((HERE / 'cases.json').read_text())['cases']


def main():
    with tempfile.TemporaryDirectory(prefix='reasoned-review-') as tmp:
        targets = []
        for case in CASES:
            path = Path(tmp) / case['name']
            path.write_text(case['source'])
            targets.append(str(path))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', *targets],
            capture_output=True, text=True, check=True)
        if result.stderr.strip():
            print(result.stderr)
        source = result.stdout
        decoder = json.JSONDecoder()
        reports = {}
        while source.strip():
            item, end = decoder.raw_decode(source.lstrip())
            source = source.lstrip()[end:]
            for file in item.get('files', []):
                reports[Path(file['path']).name] = {
                    trait['id'] for trait in file.get('traits', [])}
        failures = []
        for case in CASES:
            actual = reports.get(case['name'], set())
            missing = set(case.get('matched', [])) - actual
            unexpected = set(case.get('not_matched', [])) & actual
            if missing or unexpected:
                failures.append({'name': case['name'],
                                 'missing': sorted(missing),
                                 'unexpected': sorted(unexpected)})
        print(json.dumps({'cases': len(CASES), 'failures': failures}, indent=2))
        return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
