from pathlib import Path
import json,struct,pefile,capstone,re
rows=json.load(open('/tmp/endpoint-review-20261023/inventory.json'))
for row in rows:
 if row['sha256'][:12] not in ['41a5625a68c0','a9892231ad05']:continue
 data=Path(row['local_path']).read_bytes();pe=pefile.PE(data=data);image=pe.get_memory_mapped_image();base=pe.OPTIONAL_HEADER.ImageBase
 positions=[m.start() for m in re.finditer(re.escape(b'\xf1\xff\xff\xff\0\0\x01\x08'),image)]
 for at in positions:
  hdr=struct.unpack_from('<8Q',image,at+8);nf,nfiles,text,names,cu,files,pct,pcln=hdr
  if nf>100000 or at+pcln+nf*8>len(image):continue
  funcs=[]
  for i in range(nf):
   entry,off=struct.unpack_from('<II',image,at+pcln+i*8);n=struct.unpack_from('<i',image,at+pcln+off+4)[0];start=at+names+n
   name=image[start:image.find(b'\0',start)].decode(errors='replace');end=struct.unpack_from('<I',image,at+pcln+(i+1)*8)[0]
   funcs.append({'name':name,'va':text+entry,'size':end-entry})
  root=Path('/tmp/endpoint-review-20261023/native')/row['sha256'][:12];(root/'go-functions.json').write_text(json.dumps(funcs,indent=2))
  md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);byaddr={f['va']:f for f in funcs};calls={}
  for f in funcs:
   if f['name'].startswith(('main.','core/')):
    instructions=list(md.disasm(image[f['va']-base:f['va']-base+f['size']],f['va']));cs=[]
    for ins in instructions:
     if ins.mnemonic=='call' and ins.op_str.startswith('0x'):
      tgt=int(ins.op_str,16);cs.append({'at':hex(ins.address),'target':byaddr.get(tgt,{}).get('name',ins.op_str)})
    calls[f['name']]=cs
    fn=re.sub('[^A-Za-z0-9_.-]','_',f['name']);(root/(fn+'.asm')).write_text('\n'.join(hex(x.address)+' '+x.mnemonic+' '+x.op_str for x in instructions)+'\n')
  (root/'go-calls.json').write_text(json.dumps(calls,indent=2));print(row['sha256'][:12],len(funcs),'functions',len(calls),'application functions')
