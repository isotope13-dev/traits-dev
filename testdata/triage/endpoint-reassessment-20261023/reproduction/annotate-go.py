import json,pefile,capstone,struct,re
from pathlib import Path
rows=json.load(open('/tmp/endpoint-review-20261023/inventory.json'))
for sha in ['41a5625a68c0','a9892231ad05']:
 row=next(x for x in rows if x['sha256'].startswith(sha));pe=pefile.PE(row['local_path']);image=pe.get_memory_mapped_image();base=pe.OPTIONAL_HEADER.ImageBase;root=Path('/tmp/endpoint-review-20261023/native')/sha;fs=json.load(open(root/'go-functions.json'));byaddr={f['va']:f for f in fs};md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
 selected=[f for f in fs if f['name'].startswith(('core/','main.'))]
 annotations={}
 def get(va,n):return image[va-base:va-base+n] if base<=va<base+len(image) else b''
 for f in selected:
  ann=[]
  for ins in md.disasm(get(f['va'],f['size']),f['va']):
   comments=[]
   if ins.mnemonic=='call' and ins.op_str.startswith('0x'):comments.append(byaddr.get(int(ins.op_str,16),{}).get('name',''))
   for op in ins.operands:
    if op.type==capstone.CS_OP_MEM and op.mem.base==capstone.x86.X86_REG_RIP:
     va=ins.address+ins.size+op.mem.disp;b=get(va,16)
     if len(b)==16:
      a,n=struct.unpack('<QQ',b)
      if base<=a<base+len(image) and 0<n<4096:
       val=get(a,n);comments.append('gostring@'+hex(va)+' '+repr(val[:450]))
     if ins.mnemonic=='lea':
      b=get(va,250);ascii=b.split(b'\0')[0]
      if len(ascii)>3 and all(32<=v<127 or v in (9,10,13) for v in ascii):comments.append('literal@'+hex(va)+' '+repr(ascii[:160]))
   line=hex(ins.address)+' '+ins.mnemonic+' '+ins.op_str
   if comments:line+=' ; '+' | '.join(comments)
   ann.append(line)
  fn=re.sub('[^A-Za-z0-9_.-]','_',f['name']);(root/(fn+'.annotated')).write_text('\n'.join(ann)+'\n');annotations[f['name']]=[x for x in ann if ';' in x]
 (root/'go-annotations.json').write_text(json.dumps(annotations,indent=2))
