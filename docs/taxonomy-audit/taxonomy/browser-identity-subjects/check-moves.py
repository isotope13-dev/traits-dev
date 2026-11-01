# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify browser-identity moves preserve their effective match conditions."""
from pathlib import Path
import json
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'moves.json').read_text())
renames = {m['old']: m['new'] for m in manifest['moves']}

def normalized(value):
    if isinstance(value, list):
        return [normalized(v) for v in value]
    if isinstance(value, dict):
        return {k: normalized(v) for k, v in value.items()}
    if isinstance(value, str):
        return renames.get(value, value)
    return value

actual = {}
destinations = {m['new'].split('::')[0] for m in manifest['moves']}
paths = [path for dest in destinations for path in (ROOT / dest).glob('*.yaml')]
for path in paths:
    doc = yaml.safe_load(path.read_text()) or {}
    if not isinstance(doc, dict):
        continue
    namespace = str(path.parent.relative_to(ROOT))
    for section in ('traits', 'composite_rules'):
        for rule in doc.get(section, []) or []:
            rid = rule.get('id', '')
            if '::' not in rid:
                rid = namespace + '::' + rid
            if rid in renames.values():
                if rid in actual:
                    raise AssertionError(f'duplicate {rid}')
                actual[rid] = (doc.get('defaults') or {}, rule)

for move in manifest['moves']:
    old, new = move['old'], move['new']
    defaults, current = actual[new]
    expected = normalized(move['rule'])
    expected.pop('desc', None)
    current = dict(current)
    current.pop('desc', None)
    expected_defaults = dict(move['defaults'])
    if old.endswith('::browser-activity-upload-path'):
        expected_defaults.pop('attack', None)
    expected_effective = {**expected_defaults, **expected}
    actual_effective = {**defaults, **current}
    assert expected_effective == actual_effective, (old, expected_effective, actual_effective)
print(f"Verified {len(manifest['moves'])} moved rules and effective defaults")
