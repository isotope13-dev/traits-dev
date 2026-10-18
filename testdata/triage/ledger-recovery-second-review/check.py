"""Exercise source/sink binding and real validation/analytics near misses."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
engine = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
paths = [str(HERE / c['file']) for c in json.loads((HERE / 'cases.json').read_text())]
p = subprocess.run([engine, '--traits-dir', str(ROOT), '--format', 'json', *paths],
                   capture_output=True, text=True, check=True)
s = p.stdout
files = []
decoder = json.JSONDecoder()
while s.strip():
    item, end = decoder.raw_decode(s.lstrip())
    files.extend(item.get('files', []))
    s = s.lstrip()[end:]
observed = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])} for f in files}
for case in json.loads((HERE / 'cases.json').read_text()):
    ids = observed[case['file']]
    assert set(case['present']) <= ids, (case['file'], 'missing', set(case['present']) - ids)
    assert not set(case['absent']) & ids, (case['file'], 'unexpected', set(case['absent']) & ids)
    assert not any(t.startswith('objectives/anti-analysis/sandbox-detect/') for t in ids)
    print(case['file'], 'PASS')
