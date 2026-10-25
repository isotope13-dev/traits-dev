"""Check saved static-analysis reports; never execute fixture or sample code.
Usage: python3 check.py /path/to/version-drift-arcade/scratch
"""
import collections
import json
from pathlib import Path
import sys

scratch = Path(sys.argv[1])
migration = json.loads((Path(__file__).parent / 'migration.json').read_text())
renames = {m['old_id']: m['new_id'] for m in migration}
vbs = 'micro-behaviors/fs/path/script::vbs-filename-suffix-reference'


def reports(name):
    remaining = (scratch / name).read_text()
    decoder = json.JSONDecoder()
    while remaining.strip():
        remaining = remaining.lstrip()
        obj, end = decoder.raw_decode(remaining)
        remaining = remaining[end:]
        yield obj


def files(name):
    return [f for r in reports(name) for f in r.get('raw', r)['files']]


def traits(f, before=False):
    result = {}
    for t in f.get('traits', []):
        key = renames.get(t['id'], t['id']) if before else t['id']
        result[key] = 3 if before and key == vbs else t['crit']
    return result


def compare(old, new):
    previous, current = files(old), files(new)
    assert len(previous) == len(current), (old, len(previous), len(current))
    current = {(f['path'], f['sha']): f for f in current}
    for f in previous:
        after = current[(f['path'], f['sha'])]
        a, b = traits(f, before=True), traits(after)
        assert not (a.items() - b.items()), (f['path'], a.items() - b.items())
        assert b.keys() - a.keys() <= {vbs}, (f['path'], b.keys() - a.keys())


for before, after in [('before.json', 'after.json'),
                      ('dependency-before.json', 'dependency-after.json'),
                      ('controls-before.jsonl', 'controls-after.jsonl')]:
    compare(before, after)

extra_before = files('extra-before.jsonl') + files('more-controls-before.jsonl')
extra_after = {f['path']: f for f in files('extra-after.jsonl')}
for f in extra_before:
    assert traits(f, before=True) == traits(extra_after[f['path']]), f['path']
assert 'objectives/command-and-control/dropper/module-load::msbuild-inline-dropper' in traits(extra_after['testdata/triage/arcade-f3-version-drift/inline-task.xml'])
assert not any(t['crit'] >= 4 for t in extra_after['testdata/triage/arcade-f3-version-drift/patch-near.cs']['traits'])

boundaries = {Path(f['path']).name: traits(f) for f in files('boundaries.jsonl')}
for positive, negative, trait in [
    ('module.pl', 'module-near.pl', 'metadata/lang/source/syntax/directive::prolog-module-directive'),
    ('zip-path.sh', 'zip-near.sh', 'micro-behaviors/fs/path/temp::tmp-zip-path-literal'),
    ('wrapper.cmd', 'wrapper-near.cmd', 'micro-behaviors/fs/path/script::batch-build-powershell-script-path'),
]:
    assert trait in boundaries[positive], (positive, trait)
    assert trait not in boundaries[negative], (negative, trait)

for name in ['before.json', 'after.json', 'dependency-before.json', 'dependency-after.json']:
    fs = files(name)
    root = collections.Counter(t['crit'] for t in fs[0]['traits'])
    assert root[5] == 0 and root[4] == 1, (name, root)
    parents = {f['path'].rsplit('!!', 1)[0] for f in fs if '!!' in f['path']}
    leaf = collections.Counter(t['crit'] for f in fs if f['path'] not in parents for t in f.get('traits', []))
    assert leaf[5] == 0 and leaf[4] == 4, (name, leaf)

assert all(m['matcher_preserved'] and m['scope_preserved'] for m in migration)
print('PASS: archive observations retained, all attack controls preserved, and boundaries pass')
