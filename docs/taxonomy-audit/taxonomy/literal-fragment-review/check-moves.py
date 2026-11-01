# /// script
# dependencies = ["pyyaml"]
# ///
"""Check literal-fragment split and environment retirement."""
from collections import Counter
from pathlib import Path
import json,re,yaml
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
moves=json.loads((HERE/'moves.json').read_text())['moves']
renames={m['old']:m['new'] for m in moves}
assert len(renames)==len(moves)==len(set(renames.values()))
def normalize(v,namespace):
    if isinstance(v,list): return [normalize(i,namespace) for i in v]
    if isinstance(v,dict):
        out={}
        for k,x in v.items():
            if k=='id' and isinstance(x,str):
                if '/' not in x and '::' not in x:x=namespace+'::'+x
                out[k]=renames.get(x,x)
            else:out[k]=normalize(x,namespace)
        return out
    return v
for m in moves:
    oldns,_=m['old'].split('::'); newns,newid=m['new'].split('::')
    doc=yaml.safe_load((ROOT/m['destination']).read_text()) or {}
    match=[r for r in doc.get(m['section'],[]) if r['id']==newid]
    assert len(match)==1,m['new']
    expected={**m['defaults'],**m['before']}; actual={**(doc.get('defaults') or {}),**match[0]}
    expected.pop('id');actual.pop('id')
    if m['new_desc']:expected['desc']=m['new_desc']
    if m['new_crit']:expected['crit']=m['new_crit']
    if m['strip_attack']:
        expected.pop('attack',None);expected.pop('mbc',None)
    assert normalize(expected,oldns)==normalize(actual,newns),(m['old'],expected,actual)
counts=Counter()
for d in sorted({m['new'].split('::')[0] for m in moves}|{'objectives/command-and-control/dropper/staging/encoded/environment','metadata/lang/source/literal/fragment'}):
    for f in (ROOT/d).glob('*.yaml'):
        doc=yaml.safe_load(f.read_text()) or {}
        counts[d]+=sum(len(doc.get(k) or []) for k in ('traits','composite_rules'))
    print(d,counts[d]);assert counts[d]<72,(d,counts[d])
pattern=re.compile('(?:'+'|'.join(map(re.escape,sorted(renames,key=len,reverse=True)))+r')(?![\w-])')
for branch in ('metadata','micro-behaviors','objectives','well-known'):
    for path in (ROOT/branch).rglob('*.yaml'):
        assert not pattern.search(path.read_text()),path
print('Verified',len(moves),'moved rules and references')

assert not list((ROOT/'objectives/command-and-control/dropper/staging/encoded/environment').glob('*.yaml'))
assert not list((ROOT/'metadata/lang/source/literal/fragment').glob('*.yaml'))
print('Verified retired environment leaf and split fragment parent')
