# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify reviewed staging predicates, scopes, annotations and directory sizes."""
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
notable={'dotnet-xor-key-constant','dotnet-packed-c2-url-arrays','dotnet-xor-decoder-loop','dotnet-source-resource-payload-loader','versioned-remote-dex-stage','config-driven-remote-module-descriptor'}
suspicious={'dotnet-xor-http-stager-assembly','xor-config-silent-installer-downloader','dotnet-resource-resolve-loader','image-script-stage-hides-errors','jni-cipher-dex-classloader-writer','jni-cipher-dexpathlist-writer','jni-dex-classloader-pathlist-writer'}
for move in moves:
    source=move['old'].split('::')[0];dest=move['new'].split('::')[0];rid=move['old'].split('::')[1]
    defaults,rule=actual[move['new']]
    expected={**move['defaults'],**canonical(move['rule'],source)};current={**defaults,**canonical(rule,dest)}
    expected['id']=current['id'];expected.pop('desc',None);current.pop('desc',None);expected.pop('attack',None);expected.pop('mbc',None)
    if rid in notable:expected['crit']='notable'
    if rid in suspicious:expected['crit']='suspicious'
    if rid=='dotnet-xor-http-stager-source':expected['attack']='T1071.001,T1027'
    assert expected==current,(move['old'],expected,current)
for dest in sorted({m['new'].split('::')[0] for m in moves} | {'objectives/command-and-control/dropper/staged-loader'}):
    count=0
    for path in (ROOT/dest).glob('*.yaml'):
        data=yaml.safe_load(path.read_text()) or {}
        count+=sum(len(data.get(k) or []) for k in ('traits','composite_rules'))
    assert count<72,(dest,count)
    print(f'{dest}: {count} rules')
assert not (ROOT/'objectives/command-and-control/dropper/staging-xor').exists()
print(f'Verified {len(moves)} moves; staging-xor directory is absent')
