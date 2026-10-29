import json,struct,hashlib,re,collections
from pathlib import Path

def lzw(data,bits,expected):
 if not 2<=bits<=8:raise ValueError('LZW minimum code size outside 2..8')
 clear=1<<bits;eoi=clear+1;pos=0;width=bits+1;table={i:bytes([i]) for i in range(clear)};nxt=eoi+1;prev=None;decoded=bytearray();codes=0;ended=False
 while pos+width<=len(data)*8:
  start=pos//8;word=int.from_bytes(data[start:start+3],'little');c=(word>>(pos%8))&((1<<width)-1);pos+=width;codes+=1
  if c==clear:table={i:bytes([i]) for i in range(clear)};nxt=eoi+1;prev=None;width=bits+1;continue
  if c==eoi:ended=True;break
  if c in table:value=table[c]
  elif c==nxt and prev is not None:value=prev+prev[:1]
  else:raise ValueError(f'invalid LZW code {c} at bit {pos-width}')
  decoded.extend(value)
  if len(decoded)>expected:raise ValueError('LZW expands beyond image rectangle')
  if prev is not None and nxt<4096:
   table[nxt]=prev+value[:1];nxt+=1
   if nxt==(1<<width) and width<12:width+=1
  prev=value
 if not ended:raise ValueError('LZW end-of-information code missing')
 if len(decoded)!=expected:raise ValueError(f'pixel count {len(decoded)} != {expected}')
 return decoded,{'codes':codes,'decoded_bytes':len(decoded),'pixel_sha256':hashlib.sha256(decoded).hexdigest()}

def inspect(b):
 if b[:6] not in (b'GIF87a',b'GIF89a'):raise ValueError('not a GIF header')
 w,h,packed,bg,aspect=struct.unpack_from('<HHBBB',b,6);p=13;palettes=[];frames=[];extensions=[];all_payloads=[];total=0
 def take(n):
  nonlocal p
  if p+n>len(b):raise ValueError('truncated GIF structure')
  out=b[p:p+n];p+=n;return out
 def subblocks():
  parts=[]
  while True:
   n=take(1)[0]
   if not n:break
   parts.append(take(n))
  return b''.join(parts)
 if packed&128:palettes.append(take(3*(2**((packed&7)+1))))
 while p<len(b):
  start=p;tag=take(1)[0]
  if tag==0x3b:
   trailing=b[p:]
   return {'version':b[:6].decode(),'width':w,'height':h,'frames':frames,'extensions':extensions,'trailer_offset':p-1,'trailing_bytes':len(trailing),'trailing_hex':trailing[:128].hex(),'palette_bytes':sum(map(len,palettes)),'payload_sha256':hashlib.sha256(b).hexdigest()},all_payloads+[trailing]
  if tag==0x21:
   label=take(1)[0];payload=subblocks();extensions.append({'offset':start,'label':hex(label),'size':len(payload),'text':payload.decode('ascii','backslashreplace')[:500]});all_payloads.append(payload)
  elif tag==0x2c:
   x,y,fw,fh,fpack=struct.unpack('<HHHHB',take(9));expected=fw*fh;total+=expected
   if not fw or not fh or total>100_000_000:raise ValueError('empty or excessive image rectangle')
   if fpack&128:palettes.append(take(3*(2**((fpack&7)+1))))
   minimum=take(1)[0];compressed=subblocks();decoded,details=lzw(compressed,minimum,expected);all_payloads.append(bytes(decoded));frames.append({'offset':start,'left':x,'top':y,'width':fw,'height':fh,'interlaced':bool(fpack&64),'lzw_minimum':minimum,'compressed_bytes':len(compressed),**details})
  else:raise ValueError(f'unexpected GIF block marker {tag:#x} at {start}')
 raise ValueError('GIF trailer missing')

out=[]
for r in json.load(open('/tmp/gif-bad-triage/inventory.json')):
 b=Path(r['path']).read_bytes()
 try:
  structure,payloads=inspect(b);hits=[]
  for i,p in enumerate([b,*payloads]):
   for match in re.finditer(rb'<\?(?:php|=)|<script\b|\b(?:eval|assert|system|exec|shell_exec|passthru)\s*\(|powershell|/bin/(?:ba)?sh|[Mm][Zz]|PK\x03\x04|\x7fELF',p,re.I):hits.append({'part':i,'offset':match.start(),'match':match.group().decode('ascii','backslashreplace')})
  row={**r,'structure':structure,'content_indicators':hits}
 except Exception as e:row={**r,'error':str(e)}
 out.append(row)
Path('/tmp/gif-bad-triage/structure.json').write_text(json.dumps(out,indent=2))
print('parsed',len(out),'errors',sum('error' in r for r in out));print('dimensions',collections.Counter((r['structure']['width'],r['structure']['height']) for r in out if 'structure' in r));print('frame counts',collections.Counter(len(r['structure']['frames']) for r in out if 'structure' in r))
for r in out:
 if 'error' in r or r.get('content_indicators') or r.get('structure',{}).get('trailing_bytes') or r.get('structure',{}).get('extensions'):
  print(r['sha256'][:12],Path(r['path']).name,r.get('error'), 'frames',len(r.get('structure',{}).get('frames',[])),'tail',r.get('structure',{}).get('trailing_bytes'),'extensions',r.get('structure',{}).get('extensions',[])[:3],'indicators',r.get('content_indicators',[])[:8])
