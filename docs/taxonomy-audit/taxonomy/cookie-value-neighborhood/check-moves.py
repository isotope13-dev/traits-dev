# /// script
# dependencies = ["pyyaml"]
# ///
"""Check predicates and effective defaults for the cookie-neighborhood review."""
from pathlib import Path
import json
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'moves.json').read_text())
renames = {m['old']: m['new'] for m in manifest['moves']}
profiles = {'js-xhr-cookie-skimmer', 'obfuscated-cookie-token-remote-loader', 'js-browser-cookie-auth-xhr-exfil'}

def normalize(value):
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    return renames.get(value, value) if isinstance(value, str) else value

actual = {}
for dest in {m['new'].split('::')[0] for m in manifest['moves']}:
    for p in (ROOT / dest).glob('*.yaml'):
        data = yaml.safe_load(p.read_text()) or {}
        for section in ('traits', 'composite_rules'):
            for rule in data.get(section, []) or []:
                rid = rule['id'] if '::' in rule['id'] else dest + '::' + rule['id']
                if rid in renames.values():
                    assert rid not in actual, rid
                    actual[rid] = (data.get('defaults') or {}, rule)
for move in manifest['moves']:
    defaults, rule = actual[move['new']]
    expected = {**move['defaults'], **normalize(move['rule'])}
    current = {**defaults, **rule}
    expected['id'] = current['id']
    expected.pop('desc', None); current.pop('desc', None)
    if move['old'].split('::')[1] in profiles:
        expected.pop('attack', None); expected.pop('mbc', None)
        expected['crit'] = 'suspicious'
    assert expected == current, (move['old'], expected, current)
for dest in ['objectives/exfiltration/stealer/application-state/cookie', 'objectives/exfiltration/stealer/application-state/browser-state', 'metadata/file/profile/browser-session']:
    n=0
    for path in (ROOT / dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        n+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert n < 72, (dest, n)
    print(f'{dest}: {n} rules')
print(f"Verified {len(manifest['moves'])} moved rules and effective defaults")
