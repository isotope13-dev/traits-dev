"""Static lexical reduction only; no Lua instructions or FFI calls are executed."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parent
s=(root/'unpacked/QMRIMBYQMGNLHJNF').read_text()
pattern=r'''--\[\[.*?\]\]|--[^\r\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d+)?|[^\s]'''
tokens=[(m.group(),m.start(),m.end()) for m in re.finditer(pattern,s,re.S) if not m.group().startswith('--')]
stack=[];removed=[]
for i,(word,start,end) in enumerate(tokens):
 if word in ('function','if','for','while','repeat'):
  stack.append({'word':word,'start':start,'wait_do':word in ('for','while'),'vm':False})
 elif word=='do':
  if stack and stack[-1]['wait_do']:stack[-1]['wait_do']=False;continue
  after=[t[0] for t in tokens[i+1:i+7]]
  vm=len(after)>=5 and after[0]=='local' and after[2:4]==['=','{'] and after[4] in ('"\\065\\066\\067"','"ABC"')
  stack.append({'word':'do','start':start,'wait_do':False,'vm':vm})
 elif word in ('end','until'):
  assert stack,(word,start)
  frame=stack.pop()
  assert (word=='until')==(frame['word']=='repeat'),(frame,word,start)
  if frame['vm']:removed.append((frame['start'],end))
assert not stack,stack
# Remove only recognized self-contained VM definition blocks, after lexical
# scope matching; none is evaluated. Keep all other executable statements.
for start,end in sorted(removed,reverse=True):s=s[:start]+'\n-- omitted unused VM definition block\n'+s[end:]
# Decode escaped literals separately; this view is for inspection, not execution.
# Decimal escape decoding does not inspect or execute any Lua expression.
s=re.sub(r'\\(\d{1,3})',lambda m:chr(int(m[1])),s)
(root/'lua-reduced.txt').write_text(s)
(root/'removed-vm-blocks.json').write_text(json.dumps(removed,indent=2)+'\n')
print('Removed',len(removed),'unused VM definition blocks; remaining characters',len(s))
