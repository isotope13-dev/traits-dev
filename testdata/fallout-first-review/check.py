import json
from pathlib import Path
import subprocess
import tempfile
import shutil

root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
cases = json.loads((here / 'cases.json').read_text())
control_dir = tempfile.TemporaryDirectory(prefix='fallout-controls-', dir=root.parent.parent / 'scratch')
control_paths = []
for case in cases:
    path = Path(control_dir.name) / case['file']
    shutil.copyfile(here / case['file'], path)
    control_paths.append(str(path))
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--json', '--disable', 'third-party',
     *control_paths],
    text=True, capture_output=True, check=False)
if result.returncode:
    raise RuntimeError(result.stderr + result.stdout)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
summaries = []
for case, report in zip(cases, reports):
    def traits(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ('findings', 'traits') and isinstance(v, list):
                    for t in v:
                        if isinstance(t, dict) and 'id' in t:
                            yield t['id']
                else:
                    yield from traits(v)
        elif isinstance(x, list):
            for item in x:
                yield from traits(item)
    ids = set(traits(report))
    missing = set(case.get('required', [])) - ids
    extra = set(case.get('forbidden', [])) & ids
    assert not missing and not extra, (case['file'], missing, extra)
    summaries.append({'file': case['file'], 'required': sorted(set(case.get('required', [])) & ids), 'forbidden': sorted(extra), 'passed': True})
    print('PASS', case['file'])
assert len(reports) == len(cases), (len(reports), len(cases))
(here / 'results.json').write_text(json.dumps(summaries, indent=2) + '\n')

control_dir.cleanup()
