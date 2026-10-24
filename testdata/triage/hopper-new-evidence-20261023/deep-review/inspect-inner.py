from pathlib import Path
import dnfile,json,struct,re
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBytes
r=Path('/tmp/hopper-deep-review-20261023')
for sha in ['58d3ffd6c841','bb9830beab57']:
 p=r/(sha+'-inner-managed.dll');d=dnfile.dnPE(str(p));lines=[]
 print(sha,'CLR',bool(d.net),'ENTRY',hex(d.net.struct.EntryPointTokenOrRva) if d.net else '',flush=True)
 if not d.net:continue
 for t in d.net.mdtables.TypeDef.rows:
  for ix in t.MethodList:
   m=ix.row
   if not m.Rva:continue
   try:body=CilMethodBody(CilMethodBodyReaderBytes(d.get_data(m.Rva,65536)))
   except:continue
   lines.append(f'\nMETHOD {t.TypeNamespace}.{t.TypeName}::{m.Name} RVA {m.Rva:#x}')
   for ins in body.instructions:
    v=ins.operand
    if hasattr(v,'value'):
     n=v.value;rid=n&0xffffff;kind=n>>24
     if kind==0x70:
      try:v=repr(d.net.user_strings.get(rid).value)
      except:v=hex(n)
     else:
      tab={6:d.net.mdtables.MethodDef,10:d.net.mdtables.MemberRef,1:d.net.mdtables.TypeRef,2:d.net.mdtables.TypeDef}.get(kind)
      try:v=str(getattr(tab.rows[rid-1],'Name',getattr(tab.rows[rid-1],'TypeName',n)))
      except:v=hex(n)
    lines.append(f'{ins.offset:04x} {ins.opcode.name} {v}')
 (r/(sha+'-inner-il.txt')).write_text('\n'.join(lines));print('methods',len(d.net.mdtables.MethodDef.rows),'types',len(d.net.mdtables.TypeDef.rows),'resources',[(str(x.name),x.size) for x in d.net.resources],flush=True)
