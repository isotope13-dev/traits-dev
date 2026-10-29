import json,pathlib,struct,hashlib
r=pathlib.Path(__import__("sys").argv[1]);x=next(i for i in json.load(open(r/'inventory.json')) if i['sha256'].startswith('46641'));b=pathlib.Path(x['path']).read_bytes();s=next(s for s in x['sections'] if int(s['rva'],16)<=0x259020<int(s['rva'],16)+s['raw_size']);off=s['offset']+0x259020-int(s['rva'],16);enc=b[off:off+0xd9e00:3];key=struct.pack('<IIII',0x5a35fa4f,0xc8846ab5,0x0592b35f,0xe4f08196)
def dec(data,k):
 st=list(range(256));j=0
 for i in range(256):
  j=(j+st[i]+k[i%len(k)])&255;st[j]=st[i]
 i=j=0;out=bytearray()
 for v in data:
  i=(i+1)&255;j=(j+st[i])&255;st[j]=st[i];out.append(v^st[(st[i]+st[j])&255])
 return bytes(out)
found=[]
for arg in range(256):
 k=bytes(v^arg for v in key);p=dec(enc[:128],k)
 if p[:2]==b'MZ':
  p=dec(enc,k);q=r/f'extracted/46641dfb12c6/payload-{arg}.dll';q.parent.mkdir(exist_ok=True);q.write_bytes(p);found.append({'argument_low_byte':arg,'path':str(q),'sha256':hashlib.sha256(p).hexdigest(),'size':len(p)})
print(found);(r/'rizin/46641dfb12c6.decryption-fixed.json').write_text(json.dumps({'algorithm':'stride-3 compact -> key XOR argument -> RC4-like state overwrite (not swap)','candidates':found},indent=2)+'\n')
