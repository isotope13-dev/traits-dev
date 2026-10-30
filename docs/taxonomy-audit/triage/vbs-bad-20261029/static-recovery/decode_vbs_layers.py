"""Static array arithmetic and string slicing only; never run VBScript."""
from pathlib import Path
import ast,json,re
W=Path('/tmp/vbs-bad-triage-20261029');OUT=W/'static'
def arithmetic(expr):
 expr=re.sub(r'&H([0-9a-f]+)',r'0x\1',expr,flags=re.I)
 def go(n):
  if isinstance(n,ast.Constant)and isinstance(n.value,(int,float)):return n.value
  if isinstance(n,ast.UnaryOp):return -go(n.operand)if isinstance(n.op,ast.USub)else go(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=go(n.left),go(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
  raise ValueError('unsupported arithmetic')
 return int(go(ast.parse(expr.strip(),mode='eval').body))
evidence=[]
for p in (W/'extracted').glob('*/*.vbs'):
 s=p.read_text(errors='replace');const={m[1].lower():int(m[2])for m in re.finditer(r'(?im)^\s*const\s+(\w+)\s*=\s*(-?\d+)\s*$',s)}
 arrays={m[1].lower():m[2]for m in re.finditer(r'(?im)^(\w+)\s*=\s*Array\(([^\n]+)\)',s)}
 shift=arithmetic('((1495 - 1409.0) + (-((59 + 2615.0) - 2617.0)))')
 calls=re.findall(r'(?i)ExecuteGlobal\s*\(squander\((\w+)\)',s)
 out=[]
 for name in calls:
  vals=[int(t.strip())if re.fullmatch(r'\d+',t.strip())else const[t.strip().lower()]for t in arrays[name.lower()].split(',')]
  text=''.join(chr((x-shift)%65536)for x in vals);out.append(text)
 dst=OUT/(p.parent.name+'-array-decoded.vbs');dst.write_text('\n'.join(out));evidence.append({'input':str(p),'output':str(dst),'arrays':len(out),'offset':shift});print(p.parent.name,'arrays',len(out),'decoded bytes',dst.stat().st_size,'head',repr('\n'.join(out)[:200]))
inventory=json.loads((W/'inventory.json').read_text())
p=Path(next(x['path']for x in inventory if x['sha256'].startswith('ddc5')));s=p.read_text();blocks=[]
for start in re.finditer(r'(?m)^qwr8474\s*=\s*"([A-Z]+)"',s):
 tail=s[start.end():];chunks=[start[1]]
 for m in re.finditer(r'(?m)^qwr8474\s*=\s*qwr8474\s*&\s*"([A-Z]+)"|^ri5168\s*=',tail):
  if m[1]:chunks.append(m[1])
  else:break
 encoded=''.join(chunks);key=ord(encoded[0])-65
 # The two alphabet digits are base 25, followed by two literal offsets.
 text=''.join(chr((ord(encoded[i])-65)*25+ord(encoded[i+1])-65-key-59)for i in range(1,len(encoded),2));text=text.replace('#','');blocks.append(text)
dst=OUT/'ddc503d4e4fc-decoded.vbs';dst.write_text('\n'.join(blocks));print('DDC decoded',dst.read_text()[:1800]);evidence.append({'input':str(p),'output':str(dst),'blocks':len(blocks),'method':'verified base-25 alphabet pairs minus per-block key and offset 59; strip character 35'})
p=Path(next(x['path']for x in inventory if x['sha256'].startswith('f761')));s=p.read_text();parts=re.findall(r'(?im)^P0\s*=\s*P0\s*&\s*"((?:""|[^"])+)"',s);ps=''.join(x.replace('""','"')for x in parts);dst=OUT/'f761f760379d-layer1.ps1';dst.write_text(ps)
# The source loop selects positions 5,11,17,..., always one character.
pieces=[]
for m in re.finditer(r"\bpericyclonic\s+'([^']*)'",ps):pieces.append({'encoded':m[1],'decoded':m[1][5::6]})
(OUT/'f761f760379d-slices.json').write_text(json.dumps(pieces,indent=2));print('F761 slices',len(pieces),'\n'.join(x['decoded']for x in pieces)[:2400]);evidence.append({'input':str(p),'output':str(dst),'slice_loop':'index 5 step 6, one character','decoded_slices':pieces})
(W/'vbs-static-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
