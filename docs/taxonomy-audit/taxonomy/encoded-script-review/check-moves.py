# /// script
# dependencies = ["pyyaml"]
# ///
"""Check encoded-script moves, predicates and destination sizes."""
from collections import Counter
from pathlib import Path
import json,re,yaml
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
moves=json.loads((HERE/'moves.json').read_text())['moves']
renames={m['old']:m['new'] for m in moves}
fragment_moves=json.loads((ROOT/'docs/taxonomy-audit/taxonomy/literal-fragment-review/moves.json').read_text())['moves']
fragment_redirects={m['old']:m for m in fragment_moves}
action_moves=json.loads((ROOT/'docs/taxonomy-audit/taxonomy/action-token-review/moves.json').read_text())['moves']
action_redirects={m['old']:m for m in action_moves}
def current_id(value):
    value=action_redirects[value]['new'] if value in action_redirects else value
    return fragment_redirects[value]['new'] if value in fragment_redirects else value
followups=json.loads((ROOT/'docs/taxonomy-audit/taxonomy/wsh-fragment-review/moves.json').read_text())['moves']
followup_renames={m['old']:m['new'] for m in followups}
assert len(renames)==len(moves)==len(set(renames.values()))
def normalize(v,namespace):
    if isinstance(v,list): return [normalize(i,namespace) for i in v]
    if isinstance(v,dict):
        out={}
        for k,x in v.items():
            if k=='id' and isinstance(x,str):
                if '/' not in x and '::' not in x:x=namespace+'::'+x
                x=renames.get(x,x)
                out[k]=current_id(followup_renames.get(x,x))
            else:out[k]=normalize(x,namespace)
        return out
    return v
for m in moves:
    oldns,_=m['old'].split('::'); current=fragment_redirects.get(m['new']); newns,newid=current_id(m['new']).split('::')
    destination=current['destination'] if current else m['destination']
    doc=yaml.safe_load((ROOT/destination).read_text()) or {}
    match=[r for r in doc.get(m['section'],[]) if r['id']==newid]
    assert len(match)==1,m['new']
    expected={**m['defaults'],**m['before']}; actual={**(doc.get('defaults') or {}),**match[0]}
    expected.pop('id');actual.pop('id')
    if m['new_crit']:expected['crit']=m['new_crit']
    if m['new_desc']:expected['desc']=m['new_desc']
    if newid in {'http-ps1-url-reference','status-property-equals-200','xmlhttp-status-200-text-profile','tokenized-wsh-powershell-http-profile'}:
        expected.pop('size_max',None)
    if newid=='status-property-equals-200':
        expected.pop('unless',None)
    if newid=='comma-sharded-wsh-temp-exe-acquisition':
        group_ns='metadata/file/profile/com-encoded'
        group=yaml.safe_load((ROOT/group_ns/'wsh-fragment-review-wsh-dropper.yaml').read_text())
        combined=next(r for r in group['composite_rules'] if r['id']=='comma-sharded-wsh-com-name-clues')
        expanded=[{'id':group_ns+'::'+item['id']} for item in combined['all']]
        actual['all']=[item for leg in actual['all'] for item in (expanded if leg['id']==group_ns+'::comma-sharded-wsh-com-name-clues' else [leg])]
    if not newns.startswith('objectives/'):
        expected.pop('attack',None);expected.pop('mbc',None)
    assert normalize(expected,oldns)==normalize(actual,newns),(m['old'],expected,actual)
counts=Counter()
for d in sorted({current_id(m['new']).split('::')[0] for m in moves}|{'objectives/command-and-control/dropper/staging/encoded/script','objectives/execution/payload/file-exec/command/script-host-embedded'}):
    for f in (ROOT/d).glob('*.yaml'):
        doc=yaml.safe_load(f.read_text()) or {}
        counts[d]+=sum(len(doc.get(k) or []) for k in ('traits','composite_rules'))
    print(d,counts[d]);assert counts[d]<72,(d,counts[d])
pattern=re.compile('|'.join(map(re.escape,sorted(renames,key=len,reverse=True)))+r'(?![\w-])')
for branch in ('metadata','micro-behaviors','objectives','well-known'):
    for path in (ROOT/branch).rglob('*.yaml'):
        assert not pattern.search(path.read_text()),path
print('Verified',len(moves),'moved rules and references')
