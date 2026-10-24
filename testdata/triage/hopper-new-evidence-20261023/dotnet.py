from pathlib import Path
import dnfile,json
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBytes
r=Path('/tmp/hopper-new-review-20261023')
for sha in ['2fbd048a7cc7','98e1148702ac']:
 i=next(i for i in json.load(open(r/'inventory.json')) if i['sha256'].startswith(sha));pe=dnfile.dnPE(i['path']);out=r/'native'/sha
 tables={0x06:pe.net.mdtables.MethodDef,0x0a:pe.net.mdtables.MemberRef,0x01:pe.net.mdtables.TypeRef,0x02:pe.net.mdtables.TypeDef,0x04:pe.net.mdtables.Field}
 def token(o):
  if not hasattr(o,'value'):return str(o)
  n=o.value;kind=n>>24;rid=n&0xffffff
  if kind==0x70:
   try:return repr(pe.net.user_strings.get(rid).value)
   except:return hex(n)
  try:
   row=tables[kind].rows[rid-1];return str(getattr(row,'TypeNamespace',''))+'.'+str(getattr(row,'Name',getattr(row,'TypeName','')))
  except:return hex(n)
 lines=[]
 for n,m in enumerate(pe.net.mdtables.MethodDef.rows,1):
  if not m.Rva:continue
  try:body=CilMethodBody(CilMethodBodyReaderBytes(pe.get_data(m.Rva,65536)))
  except Exception as e:lines.append(str(e));continue
  lines.append(f'\nMETHOD {n:#x} {m.Name} RVA {m.Rva:#x}')
  for ins in body.instructions:lines.append(f'{ins.offset:04x} {ins.opcode.name} {token(ins.operand)}')
 (out/'il.txt').write_text('\n'.join(lines))
 print(sha,'methods',len(pe.net.mdtables.MethodDef.rows),'entrytoken',hex(pe.net.struct.EntryPointTokenOrRva),flush=True)
 if pe.net.mdtables.ManifestResource:
  for n,res in enumerate(pe.net.mdtables.ManifestResource.rows):
   at=pe.net.struct.ResourcesRva+res.Offset;size=int.from_bytes(pe.get_data(at,4),'little');b=pe.get_data(at+4,size);p=out/f'managed-resource-{n}.bin';p.write_bytes(b);print(str(res.Name),size,repr(b[:16]),flush=True)
