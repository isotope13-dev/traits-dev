from pathlib import Path
import json,re,pefile
inv=json.load(open('/tmp/hopper-new-review-20261023/inventory.json'))
patterns={
'field':rb'\x8b\x40\x10\x48\x89\x84\x24....',
'add':rb'\x48\x8b\x8c\x24....\x48\x8b\x94\x24....\x48\x01\xd1',
'save':rb'\x48\x89\x8c\x24....',
'call':rb'\x48\x8b\x84\x24....\x31\xdb\x31\xc9\x48\x89\xcf\xe8....'}
rows=[]
for sha in ['a58c639a1083','a5d4f63e443a','744f82adda79']:
 i=next(x for x in inv if x['sha256'].startswith(sha));b=Path(i['path']).read_bytes();p=pefile.PE(data=b);hits={k:[m.start() for m in re.finditer(v,b,re.S)] for k,v in patterns.items()};print(sha,{k:len(v) for k,v in hits.items()})
 u=lambda at:int.from_bytes(b[at:at+4],'little')
 for f in hits['field']:
  for a in hits['add']:
   if not f<a<f+512 or u(f+7)!=u(a+4):continue
   for s in hits['save']:
    if not a+19<=s<a+512:continue
    for c in hits['call']:
     if not s<c<s+1024 or u(s+4)!=u(c+4):continue
     # Reaching this is an instruction observation. Actual provenance of field
     # and native target is established separately by disassembly/emulation.
     row={'sha12':sha,'field_offset':f,'add_offset':a,'save_offset':s,'call_offset':c,'field_stack_slot':u(f+7),'target_stack_slot':u(s+4),'gaps':[a-f,s-a,c-s],'call_destination_va':p.OPTIONAL_HEADER.ImageBase+p.get_rva_from_offset(c+20)+int.from_bytes(b[c+16:c+20],'little',signed=True)};rows.append(row);print(row)
Path('/tmp/hopper-deep-review-20261023/spilled-handoff-probe.json').write_text(json.dumps(rows,indent=2))
