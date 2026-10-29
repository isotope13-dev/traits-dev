import json,struct,re,collections,hashlib
from pathlib import Path
BASE=Path('/tmp/gif-good-triage')
SIGNATURE=re.compile(rb'<\?(?:php\b|=)|<script\b|<%|\b(?:eval|assert|system|exec|shell_exec|passthru)\s*\(|powershell|/bin/(?:ba)?sh|\x7fELF|PK\x03\x04|MZ',re.I)
def inspect(b):
 w,h,packed,bg,aspect=struct.unpack_from('<HHBBB',b,6);pos=13;frames=[];extensions=[];hits=[]
 def take(n):
  nonlocal pos
  if n<0 or pos+n>len(b):raise ValueError(f'truncated block at {pos}, wants {n} bytes')
  v=b[pos:pos+n];pos+=n;return v
 def blocks():
  parts=[]
  while True:
   n=take(1)[0]
   if not n:return b''.join(parts)
   parts.append(take(n))
 if packed&128:take(3*(2**((packed&7)+1)))
 while pos<len(b):
  start=pos;tag=take(1)[0]
  if tag==0x3b:
   tail=b[pos:]
   return {'width':w,'height':h,'frames':frames,'extensions':extensions,'trailer_offset':start,'trailing_bytes':len(tail),'trailing_hex':tail[:256].hex(),'expanded_pixels':sum(f['width']*f['height'] for f in frames)},hits,tail
  if tag==0x21:
   label=take(1)[0];payload=blocks();extensions.append({'offset':start,'label':hex(label),'size':len(payload),'text':payload[:1000].decode('ascii','backslashreplace')})
   for m in SIGNATURE.finditer(payload):hits.append({'part':'extension','offset':start,'payload_offset':m.start(),'match':m.group().decode('ascii','backslashreplace')})
  elif tag==0x2c:
   x,y,fw,fh,flags=struct.unpack('<HHHHB',take(9))
   if flags&128:take(3*(2**((flags&7)+1)))
   minimum=take(1)[0];compressed=blocks();frames.append({'offset':start,'left':x,'top':y,'width':fw,'height':fh,'interlaced':bool(flags&64),'minimum_code_size':minimum,'compressed_bytes':len(compressed)})
  else:raise ValueError(f'unknown marker {tag:#x} at {start}')
 raise ValueError('GIF trailer missing')
out=[]
for row in json.loads((BASE/'inventory.json').read_text()):
 if not bytes.fromhex(row['magic_hex']).startswith((b'GIF87a',b'GIF89a')):continue
 b=Path(row['path']).read_bytes();r={**row,'raw_signatures':[{'offset':m.start(),'match':m.group().decode('ascii','backslashreplace')} for m in SIGNATURE.finditer(b)]}
 try:
  st,hits,tail=inspect(b);r.update(structure=st,metadata_signatures=hits)
  if tail:
   p=BASE/'extracted'/row['sha256'];p.mkdir(parents=True,exist_ok=True);(p/'trailing.bin').write_bytes(tail)
 except Exception as e:r['error']=str(e)
 out.append(r)
(BASE/'structure.json').write_text(json.dumps(out,indent=2)+'\n')
print('GIFs',len(out),'errors',sum('error' in r for r in out),'frames',sum(len(r.get('structure',{}).get('frames',[])) for r in out),'pixels',sum(r.get('structure',{}).get('expanded_pixels',0) for r in out))
for r in out:
 st=r.get('structure',{});interesting=[m for m in r['raw_signatures'] if m['match'].lower()!='mz']
 if r.get('error') or st.get('trailing_bytes') or r.get('metadata_signatures') or interesting:print(r['sha256'][:12],Path(r['path']).name,'error',r.get('error'),'frames',len(st.get('frames',[])),'pixels',st.get('expanded_pixels'),'tail',st.get('trailing_bytes'),'metadata',r.get('metadata_signatures',[])[:5],'raw',interesting[:5])
