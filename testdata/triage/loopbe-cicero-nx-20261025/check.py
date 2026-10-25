"""Check retained attacks, decoder variants, and documentation near misses.

Usage: python3 check.py <scratch report directory>
"""
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
def reports(*names):
 result={}
 for name in names:
  for line in (p/name).read_text().split('\n'):
   if not line:continue
   d=json.loads(line);d=d.get('raw',d);result[Path(d['files'][0]['path']).name]=d
 return result
before=reports('controls.before.json','additional-controls.before.json','native-controls.before.json')
after=reports('controls.after.json','native-controls.final.json')
clone='objectives/supply-chain/impersonation/clone-and-rename::npm-monorepo-readme-clone-publish-burst'
parasite='objectives/impact/infect/virus::inline-trampoline-feedback-parasite'
decoder='micro-behaviors/data/decode/xor::x86-multiply-rotate-feedback-xor-loop'
def traits(d):return {t['id'] for t in d['files'][0]['traits']}
for name in ['sub.exe','add.exe','lea.exe']:
 assert {parasite,decoder}<=traits(after[name]),name
for name in ['missing-feedback.exe','missing-inline.exe','nonexecutable-resource.exe']:
 assert parasite not in traits(after[name]),name
assert decoder not in traits(after['missing-feedback.exe'])
for name in ['nx-renamed.tgz','nx-foreign-repository.tgz','foreign-heading.tgz','foreign-link.tgz']:
 assert clone in traits(after[name]),name
for name in ['nx-official.tgz','product-title.tgz','self-link.tgz']:
 assert clone not in traits(after[name]),name
for name in before.keys() & after.keys():
 def high(report):
  return {(Path(f['path']).name,t['id'],t['crit']) for f in report['files'] for t in f['traits'] if t['crit']>=4}
 lost=high(before[name])-high(after[name])
 assert not lost or (name=='nx-official.tgz' and all(x[1]==clone for x in lost)),(name,lost)
print('PASS: decoder variants, clone near misses, and all retained attack coverage')
