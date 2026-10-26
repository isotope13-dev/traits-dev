from pathlib import Path
import xdis.unmarshal,xdis.magics,xdis.bytecode,xdis.op_imports,json
p=Path('/tmp/triage-new-20261024/pyinstaller/79');magic=xdis.magics.by_version['3.11'];mi=int.from_bytes(magic[:2],'little')
with open(p/'lockbitv1.marshal','rb') as f:code=xdis.unmarshal.load_code(f,mi)
op=xdis.op_imports.get_opcode_module((3,11), xdis.version_info.PythonImplementation.CPython);rows=[];lines=[]
def walk(c):
 ins=list(xdis.bytecode.Bytecode(c,op));name=c.co_name
 rows.append({'name':name,'names':list(c.co_names),'constants':[v if isinstance(v,(str,int,float,type(None),bool)) else repr(v)[:200] for v in c.co_consts],'instructions':[{'offset':x.offset,'opcode':x.opname,'arg':x.argrepr} for x in ins]})
 lines.append('\n'+name+'\n'+'\n'.join(f'{x.offset:04x} {x.opname} {x.argrepr}' for x in ins))
 for v in c.co_consts:
  if hasattr(v,'co_code'):walk(v)
walk(code);(p/'methods.json').write_text(json.dumps(rows,indent=2));(p/'methods.dis').write_text('\n'.join(lines));print([(r['name'],r['names']) for r in rows])
