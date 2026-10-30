# /// script
# dependencies = ["pyyaml"]
# ///
"""Compare recorded pre-move rules with their current effective predicates.

Usage: uv run scripts/review/check-taxonomy-move-preservation.py branch
The known multiline repair in the control-flow batch is checked separately.
"""
from pathlib import Path
import json
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
AUDITS = ROOT / 'taxonomy-migration/reviews/cap-99'
records = []
for path in sorted(AUDITS.glob('*/moves.json')):
    records.extend(json.loads(path.read_text())['moves'])
# Later moves can relocate a rule that an earlier batch already moved.
by_old = {row['old']: row for row in records}

def resolve(identifier):
    seen = set()
    while identifier in by_old and identifier not in seen:
        seen.add(identifier)
        target = by_old[identifier]['new']
        if target == identifier:
            break
        identifier = target
    return identifier

def normalize(rule, defaults, namespace):
    value = {**defaults, **rule}
    value.pop('id', None)
    value.pop('desc', None)
    def walk(item):
        if isinstance(item, list):
            return [walk(child) for child in item]
        if not isinstance(item, dict):
            return item
        result = {key: walk(child) for key, child in item.items()}
        if 'id' in result:
            ref = result['id']
            if '/' not in ref and '::' not in ref:
                ref = namespace + '::' + ref
            result['id'] = resolve(ref)
        return result
    return walk(value)

batch = sys.argv[1] if len(sys.argv) > 1 else 'branch'
before = json.loads((AUDITS / batch / 'before.json').read_text())
moves = json.loads((AUDITS / batch / 'moves.json').read_text())['moves']
lookup = {row['old']: row for row in moves}
changes = []
consolidations = []
scope_unions = []
recorded_repairs = []
for row in before:
    namespace = str(Path(row['file']).parent)
    old = namespace + '::' + row['rule']['id'].split('::')[-1]
    move = lookup[old]
    final = resolve(move['new'])
    destination = move['destination']
    # Same-ID moves also change filenames; follow those recorded locations.
    if move['new'] in by_old:
        destination = by_old[move['new']]['destination']
    if final in by_old:
        destination = by_old[final]['destination']
    path = ROOT / destination
    document = yaml.load(path.read_text(), Loader=yaml.CSafeLoader)
    current = next(rule for rule in document[row['kind']]
                   if rule['id'].split('::')[-1] == final.split('::')[-1])
    old_predicate = normalize(row['rule'], row['defaults'], namespace)
    new_predicate = normalize(current, document.get('defaults', {}), str(Path(destination).parent))
    if move.get('repair'):
        repair = move['repair']
        assert repair.get('reason') and repair.get('changes'), old
        differences = {key for key in old_predicate.keys() | new_predicate.keys()
                       if old_predicate.get(key) != new_predicate.get(key)}
        assert differences == set(repair['changes']), (old, differences, repair)
        for key, expected in repair['changes'].items():
            # Keep later relocations verifiable without freezing historical IDs.
            previous = normalize({'value': expected['before']}, {}, namespace)['value']
            updated = normalize({'value': expected['after']}, {}, str(Path(destination).parent))['value']
            assert old_predicate.get(key) == previous, (old, key, 'before')
            assert new_predicate.get(key) == updated, (old, key, 'after')
        recorded_repairs.append(old)
    elif move.get('consolidation'):
        assert old_predicate['if'] == new_predicate['if'], old
        assert old_predicate['crit'] == new_predicate['crit'] == 'notable', old
        assert set(old_predicate['platforms']) == set(new_predicate['platforms']), old
        assert old_predicate['for'] == ['ruby'] and new_predicate['for'] == ['source', 'javascript', 'ruby'], old
        # The broad predicate has no narrower size, count or suppression gate.
        assert set(new_predicate) <= {'if', 'crit', 'for', 'platforms', 'conf'}, old
        callers = yaml.load((ROOT / 'objectives/command-and-control/remote-command/client/webshell-ruby.yaml').read_text(), Loader=yaml.CSafeLoader)
        assert callers['defaults']['for'] == ['ruby'], old
        affected = [rule for rule in callers['composite_rules'] if any(condition.get('id') == final for condition in rule.get('any', []))]
        assert len(affected) == 2 and all('for' not in rule or rule['for'] == ['ruby'] for rule in affected), old
        consolidations.append(old)
    elif move.get('scope_union'):
        assert old_predicate['for'] == ['source', 'javascript'], old
        assert new_predicate['for'] == old_predicate['for'] + move['scope_union']['added_file_types'], old
        old_without_types = {key: value for key, value in old_predicate.items() if key != 'for'}
        new_without_types = {key: value for key, value in new_predicate.items() if key != 'for'}
        assert old_without_types == new_without_types, old
        scope_unions.append(old)
    elif old_predicate != new_predicate:
        changes.append(old)
expected = ['micro-behaviors/data/control-flow/loop::batch-loop-label-before-jump'] if batch == 'control-flow' else []
assert changes == expected, changes
print(f'{batch}: {len(before) - len(changes) - len(recorded_repairs) - len(consolidations) - len(scope_unions)} effective predicates/defaults preserved; {len(changes) + len(recorded_repairs)} documented repairs; {len(consolidations)} verified consolidations; {len(scope_unions)} verified scope unions')
