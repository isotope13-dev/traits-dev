"""Constant folding of independently inspected arithmetic string decoders.
This does not interpret AppleEvents, control flow, commands, or script actions.
"""
from pathlib import Path
import ast,json,re,collections
root=Path(__file__).resolve().parent
source=(root/'payload-decompiled.applescript').read_text()
def decode(name, args):
 a=args[0];b=args[1] if len(args)>1 else None;c=args[2] if len(args)>2 else None
 if name in ['dadoulrqyxid','rshxswpvpv']:v=[x-y for x,y in zip(a,b)]
 elif name in ['vfwozmlsmfbf','cvlhqofk']:v=[x+y for x,y in zip(a,b)]
 elif name=='xlgzbgvmyu':v=[x-y-c for x,y in zip(a,b)]
 elif name=='esftyhhrryyx':v=[x-b for x in a]
 elif name=='gkfocjzm':v=[a[i]-a[i+1] for i in range(0,len(a),2)]
 elif name=='ynxuypswpm':v=[y for x in a for y in [x//256,x%256] if y]
 elif name=='wzxxvakkv':v=[x-y-c for x,y in zip(a,b)][::-1]
 elif name=='xsyayloqc':v=[x-a[0] for x in a[1:]]
 elif name=='pcbjyshggyes':v=[b-x for x in a]
 elif name=='efuujxugtzlj':return bytes.fromhex(a).decode('latin1')
 else:raise ValueError(name)
 return ''.join(chr(x%65536) for x in v)
names='dadoulrqyxid|rshxswpvpv|vfwozmlsmfbf|cvlhqofk|xlgzbgvmyu|esftyhhrryyx|gkfocjzm|ynxuypswpm|wzxxvakkv|xsyayloqc|pcbjyshggyes|efuujxugtzlj'
pattern=re.compile(r'\b('+names+r')\(([^()\n]*)\)(?: of \|parent_var_1_11\|)?')
recovered=[]
def replace(m):
 try:
  args=ast.literal_eval('['+m[2].replace('{','[').replace('}',']')+']')
  s=decode(m[1],args);recovered.append({'decoder':m[1],'value':s});return json.dumps(s,ensure_ascii=True)
 except Exception:return m[0]
source=pattern.sub(replace,source)
q=r'"(?:[^"\\]|\\.)*"'
concat=re.compile(r'\(('+q+r') & ('+q+r')\)')
def fold(s):
 while True:
  out=concat.sub(lambda m:json.dumps(json.loads(m[1])+json.loads(m[2]),ensure_ascii=True),s)
  if out==s:return s
  s=out
parts=re.split(r'(?=\n={40}\nFunction:)',source)
for i,part in enumerate(parts):
 for iteration in range(8):
  part=fold(part)
  assigns=re.findall(r'^set ([A-Za-z_]\w*) to (.*)$',part,re.M)
  counts=collections.Counter(k for k,v in assigns)
  consts={k:v for k,v in assigns if counts[k]==1 and re.fullmatch(q,v)}
  if not consts:break
  # Only use a unique literal assignment after its declaration. Preserve
  # assignment destinations so each reduction remains reviewable.
  seen={};out=[]
  for line in part.splitlines():
   a=re.match(r'^(\s*set ([A-Za-z_]\w*) to )(.*)$',line)
   if a:
    tokens=re.split('('+q+')',a[3]); value=''.join(token if j%2 else re.sub(r'\b[A-Za-z_]\w*\b',lambda m:seen.get(m[0],m[0]),token) for j,token in enumerate(tokens))
    line=a[1]+value
    if a[2] in consts:seen[a[2]]=consts[a[2]]
   else:
    # Tokenize strings first to avoid replacing names within decoded data.
    tokens=re.split('('+q+')',line)
    for j in range(0,len(tokens),2):tokens[j]=re.sub(r'\b[A-Za-z_]\w*\b',lambda m:seen.get(m[0],m[0]),tokens[j])
    line=''.join(tokens)
   out.append(line)
  updated='\n'.join(out)+'\n'
  if updated==part:break
  part=updated
 parts[i]=fold(part)
(root/'payload-reduced.applescript').write_text(''.join(parts))
(root/'arithmetic-strings.json').write_text(json.dumps(recovered,indent=2)+'\n')
print('Arithmetic calls folded:',len(recovered))
