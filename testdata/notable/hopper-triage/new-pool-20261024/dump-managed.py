"""Read CIL and resources as data. Never import or execute specimen code."""
import json,sys,hashlib
from pathlib import Path
import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes
from dncil.clr.token import Token,StringToken
p=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);pe=dnfile.dnPE(str(p));tables=pe.net.mdtables
owners={id(x.row):str(t.TypeNamespace)+'.'+str(t.TypeName) for t in tables.TypeDef.rows for x in t.MethodList}
def resolve(tok):
 if isinstance(tok,StringToken):
  try:return repr(pe.net.user_strings.get(tok.rid).value)
  except:return str(tok)
 if isinstance(tok,Token):
  try:
   row=tables.tables[tok.table].rows[tok.rid-1]
   if tok.table==6:return owners.get(id(row),'')+'::'+str(row.Name)
   if tok.table==10:
    typ=row.Class.row
    owner=(str(typ.TypeNamespace)+'.'+str(typ.TypeName)) if hasattr(typ,'TypeName') else owners.get(id(typ),'')
    return owner+'::'+str(row.Name)
   return str(getattr(row,'Name',getattr(row,'TypeName',row)))
  except:return str(tok)
 return str(tok)
methods=[]
for i,m in enumerate(tables.MethodDef.rows,1):
 if not m.Rva:continue
 name=owners.get(id(m),'')+'::'+str(m.Name)
 try:
  body=read_method_body_from_bytes(pe.get_data(m.Rva,1000000));lines=[f'{x.offset:04x} {x.opcode.name} {resolve(x.operand)}' for x in body.instructions]
  (out/f'{i:04d}.il').write_text(name+'\n'+'\n'.join(lines)+'\n');methods.append({'token':hex(0x6000000+i),'name':name,'file':f'{i:04d}.il'})
 except Exception as e:methods.append({'name':name,'error':str(e)})
resources=[]
for r in pe.net.resources:
 data=r.data
 if isinstance(data,bytes):
  sha=hashlib.sha256(data).hexdigest();(out/sha).write_bytes(data);resources.append({'name':str(r.name),'size':len(data),'sha256':sha})
(out/'index.json').write_text(json.dumps({'entrypoint':hex(pe.net.struct.EntryPointTokenOrRva),'methods':methods,'resources':resources},indent=2))
print(json.dumps({'methods':len(methods),'resources':resources},indent=2))
