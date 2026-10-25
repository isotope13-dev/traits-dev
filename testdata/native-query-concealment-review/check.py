"""Positive and near-miss checks for each distinct native behavior."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HOOK = 'objectives/evasion/process/hook/inline::'
HIDE = HOOK+'image-extension-query-denial-trampoline'
PATCH = HOOK+'decoded-hotpatch-status-return-override'
ATOM = HOOK+'decoded-hotpatch-status-return-patch'
LOAD = 'objectives/execution/payload/process-inject::memory-concealing-pe-thread-loader'
EXPECTED = {
    'all-behaviors': {HIDE, PATCH, LOAD, ATOM},
    'different-key': {HIDE, PATCH, LOAD, ATOM},
    'unrelated-api': {HIDE, LOAD},
    'query-only': {HIDE},
    'thread-only': set(),
    'hash-only': set(),
    'hotpatch-only': {ATOM},
    'different-query-class': set(),
    'hex-xor': set(),
    'bare-xor': set(),
}
paths = [str(HERE.parent/('hostile' if label in {'all-behaviors', 'different-key', 'unrelated-api', 'query-only', 'hotpatch-only'} else 'benign')/HERE.name/(label+'.exe')) for label in EXPECTED]
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                         '--json', *paths], capture_output=True, text=True, check=True)
reports = [f for line in result.stdout.split('\n') if line.strip() for f in json.loads(line)['files']]
for f in reports:
    ids = {t['id'] for t in f.get('traits', [])}
    actual = ids & {HIDE, PATCH, LOAD, ATOM}
    codec = 'micro-behaviors/data/decode/xor::hex-pairs-cyclic-key-xor'
    if Path(f['path']).stem in ['hex-xor', 'bare-xor']:
        assert (codec in ids) == (Path(f['path']).stem == 'hex-xor')
    assert actual == EXPECTED[Path(f['path']).stem], (f['path'], actual)
print('PASS: ten native controls; key changes retain coverage; API/class near misses reject')
