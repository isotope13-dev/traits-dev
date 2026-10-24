"""Preserve source-shape evidence and the existing encrypted-loader consumer."""
import os
from pathlib import Path
import subprocess
import tempfile
import sys
sys.dont_write_bytecode = True
from check import ROOT, reports

MOVED = 'metadata/lang/source/syntax/call/arguments::computed-call-hex-token-pairs'
OLD = 'micro-behaviors/data/control-flow/dispatch::computed-call-hex-token-pairs'
ATTACK = 'objectives/command-and-control/dropper/module-load::packed-aead-envelope-module-loader'
BASE = Path(__file__).with_name('placement')
CASES = {
    'three-call-shapes.js': (True, False),
    'quoted-call-shapes.js': (True, False),
    'two-call-shapes.js': (False, False),
    'nonhex-arguments.js': (False, False),
    'envelope-loader.js': (True, True),
}
workspace = tempfile.TemporaryDirectory(prefix='source-shape-placement-')
paths = []
for name in CASES:
    path = Path(workspace.name) / name
    path.write_bytes((BASE / name).read_bytes())
    paths.append(path)
paths += [ROOT / 'testdata/hostile/npm-math-universe-aes-stage-loader.tgz',
          ROOT / 'testdata/benign/buffer-fixed-offset-slice.js']
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                         '--format', 'json', *map(str, paths)],
                        capture_output=True, text=True, check=True, timeout=180)
checked = set()
for f in reports(result.stdout):
    ids = {t['id'] for t in f.get('traits', [])}
    assert OLD not in ids
    name = Path(f['path']).name
    if name in CASES:
        want_shape, want_attack = CASES[name]
        assert (MOVED in ids, ATTACK in ids) == (want_shape, want_attack), (name, ids)
        checked.add(name)
    if f['path'] == str(paths[-2]):
        assert MOVED in ids and ATTACK in ids
        checked.add('retained-encrypted-loader')
    if f['path'] == str(paths[-1]):
        assert MOVED not in ids and ATTACK not in ids
        checked.add('benign-buffer-slices')
assert len(checked) == 7, checked
workspace.cleanup()
print('7 source-placement and retained-loader controls passed')
