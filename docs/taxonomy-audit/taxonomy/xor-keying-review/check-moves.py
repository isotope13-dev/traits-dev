# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify the XOR split, its effective rule definitions, and directory sizes."""
from collections import Counter
import json
from pathlib import Path
import re
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
moves = json.loads((HERE / 'moves.json').read_text())['moves']
renames = {m['old']: m['new'] for m in moves}
assert len(renames) == len(moves) == len(set(renames.values()))

def normalize(value, namespace):
    if isinstance(value, list):
        return [normalize(v, namespace) for v in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key == 'id' and isinstance(item, str):
                if '/' not in item and '::' not in item:
                    item = namespace + '::' + item
                result[key] = renames.get(item, item)
            else:
                result[key] = normalize(item, namespace)
        return result
    return value

for move in moves:
    oldns, oldid = move['old'].split('::')
    newns, newid = move['new'].split('::')
    doc = yaml.safe_load((ROOT / move['destination']).read_text()) or {}
    matches = [r for sec in ('traits', 'composite_rules') for r in doc.get(sec, []) or [] if r['id'] == newid]
    assert len(matches) == 1, move['new']
    expected = {**move['defaults'], **move['rule']}
    actual = {**(doc.get('defaults') or {}), **matches[0]}
    expected.pop('id'); actual.pop('id')
    if oldns == 'micro-behaviors/data/decode/xor':
        # Direction-neutral observations have no deobfuscation ATT&CK claim.
        expected.pop('attack', None)
        expected.pop('desc', None); actual.pop('desc', None)
    if oldid == 'js-byte-array-xor-map':
        expected.pop('desc', None); actual.pop('desc', None)
    assert normalize(expected, oldns) == normalize(actual, newns), move['old']

counts = Counter()
for directory in {m['new'].split('::')[0] for m in moves} | {'micro-behaviors/data/decode/xor'}:
    for path in (ROOT / directory).glob('*.yaml'):
        doc = yaml.safe_load(path.read_text()) or {}
        counts[directory] += sum(len(doc.get(k) or []) for k in ('traits', 'composite_rules'))
    assert counts[directory] < 72, (directory, counts[directory])
    print(f'{directory}: {counts[directory]} rules')
assert not list((ROOT / 'micro-behaviors/data/encoding/xor').glob('*.yaml'))
pattern = re.compile('|'.join(re.escape(k) for k in sorted(renames, key=len, reverse=True)) + r'(?![\w-])')
for branch in ('metadata', 'micro-behaviors', 'objectives', 'well-known'):
    for path in (ROOT / branch).rglob('*.yaml'):
        assert not pattern.search(path.read_text()), path
print(f'Verified {len(moves)} moved rules and references')
