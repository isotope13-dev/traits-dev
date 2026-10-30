"""Recover constant JSO decoder calls using only arithmetic, Base64 and RC4.
No JavaScript interpreter or sample code is invoked.
"""
import ast, base64, json, math, re, sys
from pathlib import Path
TOK=re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|//[^\n]*|/\*[\s\S]*?\*/|[A-Za-z_$][\w$]*|0x[0-9a-fA-F]+|\d+(?:\.\d+)?|[^\s]")
class Unknown(Exception):pass
def num(x):
 if isinstance(x,(int,float)):return x
 if isinstance(x,str):
  try:return int(x,0) if x.lower().startswith(('0x','-0x'))else float(x)
  except ValueError:return float('nan')
 raise Unknown()
def rc4(text,key):
 s=list(range(256));j=0
 for i in range(256):j=(j+s[i]+ord(key[i%len(key)]))%256;s[i],s[j]=s[j],s[i]
 out=[];i=j=0
 for c in text:
  i=(i+1)%256;j=(j+s[i])%256;s[i],s[j]=s[j],s[i];out.append(chr(ord(c)^s[(s[i]+s[j])%256]))
 return ''.join(out)
class Decoder:
 def __init__(self,source):
  toks=[m for m in TOK.finditer(source)if not m[0].startswith(('//','/*'))];self.source=source;self.functions={};self.roots={};self.tables={};self.rotation={};self.strings=set();self.cache={}
  for n,t in enumerate(toks):
   if t[0]!='function' or n+2>=len(toks)or toks[n+2][0]!='(':continue
   name=toks[n+1][0];k=n+3;params=[]
   while k<len(toks)and toks[k][0]!=')':
    if toks[k][0]!=',':params.append(toks[k][0])
    k+=1
   if k+1>=len(toks)or toks[k+1][0]!='{':continue
   depth=1;start=k+2;end=start
   while end<len(toks)and depth:
    if toks[end][0]=='{':depth+=1
    if toks[end][0]=='}':depth-=1
    end+=1
   body=source[toks[k+1].end():toks[end-1].start()]
   if re.fullmatch(r'\s*return\s+[^;]+;?\s*',body):self.functions[name]=(params,re.sub(r'^\s*return\s+','',body).strip().rstrip(';'))
   a=re.match(r'\s*var\s+(\w+)\s*=\s*\[([\s\S]*?)\]\s*;',body)
   if a:
    try:
     vals=ast.literal_eval('['+a[2]+']')
     if len(vals)>30 and all(isinstance(x,str)for x in vals):self.tables[name]=vals;self.rotation[name]=0
    except (ValueError,SyntaxError):pass
   a=re.match(r'\s*var\s+\w+\s*=\s*(\w+)\(\);\s*'+re.escape(name)+r'\s*=\s*function\s*\((\w+)\s*,\s*\w+\)\s*\{\s*\2\s*=\s*\2\s*-\s*([^;]+);',body)
   if a:self.roots[name]=(a[1],self.eval(a[3],{}),'charCodeAt' in body and '^'in body)
  if not self.roots or not self.tables:raise Unknown('no recognized string decoder')
  self.align()
 def eval(self,expr,env,depth=0):
  if depth>40:raise Unknown('recursion limit')
  try:node=ast.parse(expr.strip(),mode='eval').body
  except SyntaxError:raise Unknown('unsupported expression')
  def walk(n):
   if isinstance(n,ast.Constant)and isinstance(n.value,(int,float,str)):return n.value
   if isinstance(n,ast.Name)and n.id in env:return env[n.id]
   if isinstance(n,ast.UnaryOp):
    v=num(walk(n.operand))
    if isinstance(n.op,ast.USub):return -v
    if isinstance(n.op,ast.UAdd):return v
   if isinstance(n,ast.BinOp):
    a=walk(n.left);b=walk(n.right)
    if isinstance(n.op,ast.Add):return str(a)+str(b)if isinstance(a,str)or isinstance(b,str)else a+b
    a=num(a);b=num(b)
    if isinstance(n.op,ast.Sub):return a-b
    if isinstance(n.op,ast.Mult):return a*b
    if isinstance(n.op,ast.Div):return a/b
    if isinstance(n.op,ast.Mod):return a%b
   if isinstance(n,ast.Call)and isinstance(n.func,ast.Name):
    name=n.func.id;args=[walk(x)for x in n.args]
    if name=='parseInt':
     m=re.match(r'^\s*([+-]?\d+)',str(args[0]));return int(m[1])if m else float('nan')
    if name in self.roots:
     table,offset,encrypted=self.roots[name];i=int(num(args[0])-offset);values=self.tables[table];idx=(i+self.rotation[table])%len(values)
     if not 0<=i<len(values):raise Unknown('array index out of range')
     ck=(table,idx,encrypted,str(args[1])if encrypted else '')
     if ck not in self.cache:
      v=values[idx];custom='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/';standard='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
      b=base64.b64decode(v.translate(str.maketrans(custom,standard))+'='*((-len(v))%4));text=b.decode('utf-8')
      self.cache[ck]=rc4(text,str(args[1]))if encrypted else text
     return self.cache[ck]
    if name in self.functions:
     ps,body=self.functions[name]
     if len(args)!=len(ps):raise Unknown('argument count')
     return self.eval(body,dict(zip(ps,args)),depth+1)
   raise Unknown(type(n).__name__)
  return walk(node)
 def align(self):
  # Only the arithmetic checksum expression is evaluated. No loop body or
  # arbitrary source statement is executed.
  for table in self.tables:
   call=re.search(r'\}\(\s*'+re.escape(table)+r'\s*,\s*([^;]+)\)\);',self.source)
   if not call:continue
   target=self.eval(call[1],{})
   checks=re.findall(r'var\s+\w+\s*=\s*([^;]*parseInt\([^;]+);',self.source)
   found=False
   for check in checks:
    for rotation in range(len(self.tables[table])):
     self.rotation[table]=rotation
     try:value=self.eval(check,{})
     except (Unknown,ValueError,UnicodeError,ZeroDivisionError):continue
     if math.isfinite(value)and abs(value-target)<0.00001:found=True;break
    if found:break
   if not found:raise Unknown('rotation not established')
 def recover(self):
  source=self.source;repls=[]
  for m in re.finditer(r'\b([A-Za-z_$][\w$]*)\(',source):
   if m[1]not in self.functions and m[1]not in self.roots:continue
   depth=1;i=m.end();quote=None
   while i<len(source)and i-m.start()<1200 and depth:
    c=source[i]
    if quote:
     if c=='\\':i+=2;continue
     if c==quote:quote=None
    elif c in "'\"":quote=c
    elif c=='(':depth+=1
    elif c==')':depth-=1
    i+=1
   if depth:continue
   try:v=self.eval(source[m.start():i],{})
   except (Unknown,ValueError,UnicodeError,ZeroDivisionError):continue
   if isinstance(v,str):self.strings.add(v);repls.append((m.start(),i,json.dumps(v)))
  end=len(source)+1
  for a,b,v in reversed(repls):
   if b<=end:source=source[:a]+v+source[b:];end=a
  literal=re.compile(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")\s*\+\s*('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")")
  for _ in range(30):
   updated=literal.sub(lambda m:json.dumps(ast.literal_eval(m[1])+ast.literal_eval(m[2])),source)
   if updated==source:break
   source=updated
  return source
if __name__=='__main__':
 for raw in sys.argv[1:]:
  p=Path(raw)
  try:
   d=Decoder(p.read_text());text=d.recover();p.with_suffix('.recovered.js').write_text(text);p.with_suffix('.strings.json').write_text(json.dumps(sorted(d.strings),indent=2));print(p.name,'strings',len(d.strings),'rotations',d.rotation,'interesting',[x for x in d.strings if re.search('(?i)https?:|powershell|cmd|\.exe|wscript|ADODB|XMLHTTP|Sleep|CreateObject',x)])
  except Exception as e:print(p.name,type(e).__name__,str(e))
