# /// script
# dependencies = ["pyyaml"]
# ///
"""Compare relocated token-neighborhood rules and effective defaults."""
from pathlib import Path
import json
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
moves = json.loads((HERE / 'moves.json').read_text())['moves']
renames = {m['old']: m['new'] for m in moves}

def normalize(value):
    if isinstance(value, list): return [normalize(v) for v in value]
    if isinstance(value, dict): return {k: normalize(v) for k,v in value.items()}
    return renames.get(value, value) if isinstance(value, str) else value

actual={}
for dest in {m['new'].split('::')[0] for m in moves}:
    for path in (ROOT / dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        for section in ('traits','composite_rules'):
            for rule in data.get(section,[]) or []:
                rid=rule['id'] if '::' in rule['id'] else dest+'::'+rule['id']
                if rid in renames.values():
                    assert rid not in actual, rid
                    actual[rid]=(data.get('defaults') or {},rule)
for move in moves:
    defaults,rule=actual[move['new']]
    expected={**move['defaults'],**normalize(move['rule'])}
    current={**defaults,**rule}
    expected['id']=current['id']
    expected.pop('desc',None);current.pop('desc',None)
    if move['new'].startswith('metadata/'):
        expected.pop('attack',None);expected.pop('mbc',None)
        if expected.get('crit')=='hostile':expected['crit']='suspicious'
    if move['old'].split('::')[1] in {
        'rust-telegram-session-archive-upload',
        'rust-fixed-bot-session-archive-upload',
        'rust-xor-bot-session-archive-upload',
        'rust-session-archive-fixed-multipart-upload',
    }:
        expected['attack']='T1041,T1567'
    assert expected==current,(move['old'],expected,current)
for dest in sorted({m['new'].split('::')[0] for m in moves} | {'objectives/exfiltration/stealer/credential/value/token'}):
    n=0
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        n+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert n<72,(dest,n)
    print(f'{dest}: {n} rules')
print(f'Verified {len(moves)} moved rules and effective defaults')
