from pathlib import Path
import pefile,json,struct,hashlib
p=Path('/tmp/triage-new-20261024');r=json.load(open(p/'inventory.json'));pe=pefile.PE(r[70]['path']);base=pe.OPTIONAL_HEADER.ImageBase;key=pe.get_data(0xe320,16);table=0x14000212b+0x264e4bd
print('RC4 key',key.hex(),'table VA',hex(table),flush=True)
out=p/'swift-payloads';out.mkdir(exist_ok=True);records=[]
def rc4(data,key):
 s=list(range(256));j=0
 for i in range(256):j=(j+s[i]+key[i%len(key)])&255;s[i],s[j]=s[j],s[i]
 i=j=0;v=bytearray()
 for c in data:
  i=(i+1)&255;j=(j+s[i])&255;s[i],s[j]=s[j],s[i];v.append(c^s[(s[i]+s[j])&255])
 return bytes(v)
for i in range(10):
 at=table-base+i*16;addr,size=struct.unpack('<QI',pe.get_data(at-8,12));print(i,hex(addr),size,flush=True)
 if not base<=addr<base+pe.OPTIONAL_HEADER.SizeOfImage or not 0<size<64*1024*1024:continue
 data=rc4(pe.get_data(addr-base,size),key);fn=out/f'{i}.exe';fn.write_bytes(data);records.append({'index':i,'pointer':hex(addr),'size':len(data),'prefix':data[:8].hex(),'sha256':hashlib.sha256(data).hexdigest(),'path':str(fn)})
(p/'swift-recovery.json').write_text(json.dumps(records,indent=2)+'\n')
