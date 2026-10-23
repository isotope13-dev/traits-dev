"""Static fixture checks; the analyzed commands are never executed."""
import json
from pathlib import Path
import subprocess
import shutil
import tempfile
import sys

here = Path(__file__).resolve().parent
root = here.parents[2]
cases = json.loads((here / 'cases.json').read_text())['fixtures']
# Stage outside testdata so explicit fixture-path suppressors do not hide the
# launch observation being tested. Only scanner inputs are copied or read.
staging = tempfile.TemporaryDirectory(prefix='operation-controls-',
                                     dir=sys.argv[2] if len(sys.argv) > 2 else None)
staged = Path(staging.name)
for case in cases:
    source = root / case['path']
    shutil.copyfile(source, staged / source.name)
result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave',
                         '--traits-dir', str(root), '--format', 'json', str(staged)],
                        check=True, capture_output=True, text=True)
reports = {}
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report.get('files', []):
        reports[Path(file['path']).resolve()] = {
            trait['id']: trait['crit'] for trait in file.get('traits', [])}
for case in cases:
    traits = reports[(staged / Path(case['path']).name).resolve()]
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not (missing or unexpected), (case['path'], missing, unexpected)
    assert max(traits.values(), default=0) <= case['max_crit'], case['path']
    print(Path(case['path']).name + ': PASS')
print(str(len(cases)) + ' operation-placement controls passed')

staging.cleanup()
