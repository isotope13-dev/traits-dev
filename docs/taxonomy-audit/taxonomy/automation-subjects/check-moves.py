# /// script
# dependencies = ["pyyaml"]
# ///
"""Check automation-rule moves, including intentional severity changes."""
from pathlib import Path
import json
import yaml
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
moves=json.loads((HERE/'moves.json').read_text())['moves']
renames={m['old']:m['new'] for m in moves}

def canonical(value,namespace):
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
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        for section in ('traits','composite_rules'):
            for rule in data.get(section,[]) or []:
                rid=rule['id'] if '::' in rule['id'] else dest+'::'+rule['id']
                if rid in renames.values():
                    assert rid not in actual,rid
                    actual[rid]=(data.get('defaults') or {},rule)
for move in moves:
    src=move['old'].split('::')[0];dest=move['new'].split('::')[0]
    defaults,rule=actual[move['new']]
    expected={**move['defaults'],**canonical(move['rule'],src)}
    current={**defaults,**canonical(rule,dest)}
    expected['id']=current['id'];expected.pop('desc',None);current.pop('desc',None)
    expected.pop('attack',None);expected.pop('mbc',None)
    if move['source']=='defender-kql.yaml' or move['old'].endswith('::n8n-execution-data-api-path'):
        expected['crit']='notable'
    if move['old'].split('::')[1] in {'n8n-api-workflow-takeover-cleanup','n8n-api-credential-execution-harvest','skill-covertly-stores-private-agent-thoughts'}:
        expected['crit']='suspicious'
    assert expected==current,(move['old'],expected,current)
for dest in sorted({m['new'].split('::')[0] for m in moves}):
    count=0
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        count+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert count<72,(dest,count)
    print(f'{dest}: {count} rules')
assert not list((ROOT/'objectives/exfiltration/sensitive-data/automation').rglob('*.yaml'))
print(f'Verified {len(moves)} moves; legacy automation leaf contains no YAML rules')
