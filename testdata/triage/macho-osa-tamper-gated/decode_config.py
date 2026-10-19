"""Evaluate data assignments and crypto recipes in the inspected config setter.
Only integer expressions, stack bytes, HKDF and authenticated decryption are
supported. No native calls, script code, or external commands are interpreted.
"""
from pathlib import Path
import re,ast,operator,json
import decode_payload as d
root=d.ROOT;src=(root/'decompiled/1000989bc.c').read_text()
widths={name:int(n) for n,name in re.findall(r'undefined(\d+)\s+((?:local|uStack)_[a-f0-9]+);',src)}
mem={}
def address(name):return -int(name.split('_')[1],16)
def getmem(name,n=None,off=0):return bytes(mem.get(address(name)+off+i,0) for i in range(n or widths[name]))
def putmem(name,data,off=0):
 for i,b in enumerate(data):mem[address(name)+off+i]=b
def cint(name):return int.from_bytes(getmem(name),'little')
ops={ast.LShift:operator.lshift,ast.RShift:operator.rshift,ast.BitXor:operator.xor,ast.BitOr:operator.or_,ast.BitAnd:operator.and_,ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul}
def expr(s):
 s=s.replace('_UNK_','DAT_')
 s=re.sub(r'\((?:undefined\d+|uint\d*|ulong|long|int|byte)\)','',s)
 s=re.sub(r'((?:local|uStack|DAT)_[a-f0-9]+)\._(\d+)_(\d+)_',lambda m:f'FIELD({m[1]}, {m[2]}, {m[3]})',s)
 def walk(n):
  if isinstance(n,ast.Constant) and isinstance(n.value,int):return n.value
  if isinstance(n,ast.Name):
   if n.id in widths:return cint(n.id)
   if n.id.startswith('DAT_'):return int.from_bytes(d.read(int(n.id[4:],16),8),'little')
  if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](walk(n.left),walk(n.right))
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -walk(n.operand)
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
   if n.func.id=='FIELD':
    name=n.args[0].id;off=walk(n.args[1]);size=walk(n.args[2]);return int.from_bytes(d.read(int(name[4:],16)+off,size) if name.startswith('DAT_') else getmem(name,size,off),'little')
   if re.fullmatch(r'CONCAT\d\d',n.func.id):
    a,b=map(int,n.func.id[-2:]);return ((walk(n.args[0])&((1<<(a*8))-1))<<(b*8))|(walk(n.args[1])&((1<<(b*8))-1))
  raise ValueError(ast.dump(n))
 return walk(ast.parse(s.strip(),mode='eval').body)
key=bytes.fromhex(json.loads((root/'key-recovery.json').read_text())['key_hex'])
result={};last_plain=None
for lineno,line in enumerate(src.splitlines(),1):
 m=re.match(r'\s*((?:local|uStack)_[a-f0-9]+)(?:\._(\d+)_(\d+)_)??\s*=\s*(.*);$',line)
 if m and m[1] in widths:
  try:
   v=expr(m[4]);size=int(m[3]) if m[3] else widths[m[1]];off=int(m[2] or 0)
   putmem(m[1],(v&((1<<(size*8))-1)).to_bytes(size,'little'),off)
  except (ValueError,SyntaxError):pass
 m=re.search(r'FUN_10009380c\(param_1,0x20,0,0,&(\w+),0x11,&(\w+),0xc\)',line)
 if m:putmem(m[2],d.hkdf(key,b'',getmem(m[1],17),12))
 m=re.search(r'FUN_100093c00\(param_1,&(\w+),&(\w+),(0x[0-9a-f]+|\d+),&(\w+),&(\w+)\)',line)
 if m:
  size=int(m[3],0);plain=d.decrypt(key,getmem(m[1],12),getmem(m[2],size),getmem(m[4],16));putmem(m[5],plain);last_plain=plain
 m=re.search(r'\(\*pcVar1\)\(&(\w+),&(\w+),1\)',line)
 if m:
  name=getmem(m[1],48).split(b'\0')[0].decode();value=getmem(m[2],128).split(b'\0')[0].decode();result[name]=value
(root/'decoded-config.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
