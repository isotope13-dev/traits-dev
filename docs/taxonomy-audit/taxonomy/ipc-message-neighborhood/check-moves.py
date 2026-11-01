# /// script
# dependencies = ["pyyaml"]
# ///
"""Compare relocated messaging and storage predicates and effective defaults."""
from pathlib import Path
import json
import yaml

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
moves=json.loads((HERE/'moves.json').read_text())['moves']
renames={m['old']:m['new'] for m in moves}

def canonical(value, namespace):
    if isinstance(value,list):return [canonical(v,namespace) for v in value]
    if isinstance(value,dict):
        result={}
        for k,v in value.items():
            if k=='id' and isinstance(v,str):
                full=namespace+'::'+v if '::' not in v and '/' not in v else v
                result[k]=renames.get(full,full)
            else:result[k]=canonical(v,namespace)
        return result
    return value

actual={}
for dest in {m['new'].split('::')[0] for m in moves}:
    for p in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(p.read_text()) or {}
        for section in ('traits','composite_rules'):
            for rule in data.get(section,[]) or []:
                rid=rule['id'] if '::' in rule['id'] else dest+'::'+rule['id']
                if rid in renames.values():
                    assert rid not in actual,rid
                    actual[rid]=(data.get('defaults') or {},rule)
for move in moves:
    old_ns=move['old'].split('::')[0];dest=move['new'].split('::')[0]
    defaults,rule=actual[move['new']]
    expected={**move['defaults'],**canonical(move['rule'],old_ns)}
    current={**defaults,**canonical(rule,dest)}
    expected['id']=current['id']
    expected.pop('desc',None);current.pop('desc',None)
    if move['old'].endswith('::page-content-message-relay'):
        expected.pop('attack',None);expected.pop('mbc',None)
    assert expected==current,(move['old'],expected,current)
for dest in sorted({m['new'].split('::')[0] for m in moves} | {'micro-behaviors/communications/ipc/message','micro-behaviors/data/db/access'}):
    count=0
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        count+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert count<72,(dest,count)
    print(f'{dest}: {count} rules')
print(f'Verified {len(moves)} moved rules and effective defaults')
