"""Check focused rules, including OR composites omitted from scan rendering."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
cleave = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
for case in cases['fixtures']:
    rules = case['matched'] + case['not_matched']
    result = subprocess.run(
        [cleave, '--traits-dir', str(root), 'test-rules',
         str(root / case['path']), '--rules', ','.join(rules)],
        cwd=root, capture_output=True, text=True,
        env={**os.environ, 'NO_COLOR': '1'}, check=True,
    )
    assert "Warning: Rule '" not in result.stdout + result.stderr, result.stdout
    matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
    missing = set(case['matched']) - matched
    unexpected = set(case['not_matched']) & matched
    assert not missing and not unexpected, (case['path'], missing, unexpected, result.stdout)
    print('PASS', Path(case['path']).name, flush=True)
print(f"{len(cases['fixtures'])} focused controls passed")
