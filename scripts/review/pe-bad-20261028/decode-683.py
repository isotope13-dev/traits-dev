import json,pathlib,re
r=pathlib.Path(__import__("sys").argv[1]);a=json.load(open(r/'inventory.json'));x=next(i for i in a if i['sha256'].startswith('683a09'));b=pathlib.Path(x['path']).read_bytes();out=[]
for s in x['sections']:
 if s['flags']=='0x60000020':continue
 lo=s['offset'];hi=min(len(b),lo+s['raw_size'])
 for o in range(lo,hi-10):
  n=b[o+1];key=b[o]
  if not 5<=n<=127 or o+5+n>hi:continue
  raw=b[o+5:o+5+n];d=bytes(((v^key)-j-1)&255 for j,v in enumerate(raw))
  if all(32<=c<127 for c in d):out.append({'offset':o,'va':hex(0x400000+int(s['rva'],16)+o-lo),'key':key,'length':n,'value':d.decode()})
(r/'rizin/683a09da2199.decoded-strings.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2)[:10000])
