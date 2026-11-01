# /// script
# dependencies = ["pyyaml"]
# ///
"""Check encrypted-staging and XOR-neighborhood moves."""
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
        out={}
        for k,v in value.items():
            if k=='id' and isinstance(v,str):
                full=namespace+'::'+v if '::' not in v and '/' not in v else v
                out[k]=renames.get(full,full)
            else:out[k]=canonical(v,namespace)
        return out
    return value
actual={}
for dest in {m['new'].split('::')[0] for m in moves}:
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        for sec in ('traits','composite_rules'):
            for rule in data.get(sec,[]) or []:
                rid=rule['id'] if '::' in rule['id'] else dest+'::'+rule['id']
                if rid in renames.values():
                    assert rid not in actual,rid
                    actual[rid]=(data.get('defaults') or {},rule)
notable={'hardcoded-aes-key','aes-file-extension','powershell-hex-xor-decoder','powershell-scalar-hex-xor-decoder','powershell-regex-hex-xor-decoder'}
suspicious={'go-crypter-encrypted-payload-staging','aes-ctr-antidebug-temp-exe-dropper','powershell-hex-xor-command-loader','padded-powershell-hex-xor-stager','html-hex-decoded-file-stage','html-hex-decoded-payload-dropper'}
for move in moves:
    source,rid=move['old'].split('::');dest=move['new'].split('::')[0]
    defaults,rule=actual[move['new']]
    expected={**move['defaults'],**canonical(move['rule'],source)};current={**defaults,**canonical(rule,dest)}
    expected['id']=current['id'];expected.pop('desc',None);current.pop('desc',None)
    if move['source']!='sibling-evm-encrypted-chunks.yaml':expected.pop('attack',None);expected.pop('mbc',None)
    if rid in notable:expected['crit']='notable'
    if rid in suspicious:expected['crit']='suspicious'
    if rid=='embedded-python-bytecode-dropper':expected['attack']='T1027,T1140,T1059.006'
    assert expected==current,(move['old'],expected,current)
for dest in sorted({m['new'].split('::')[0] for m in moves}|{'objectives/command-and-control/dropper/staging/encrypted','micro-behaviors/data/decode/xor'}):
    count=0
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        count+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert count<80,(dest,count)
    print(f'{dest}: {count} rules')
print(f'Verified {len(moves)} moves and effective defaults')
