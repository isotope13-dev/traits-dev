from pathlib import Path
import ast,json,zipfile
rows=json.load(open('/tmp/endpoint-review-20261023/inventory.json'))
class StripDocs(ast.NodeTransformer):
 def visit_Module(self,node):
  self.generic_visit(node);node.body=[x for i,x in enumerate(node.body) if not(i==0 and isinstance(x,ast.Expr) and isinstance(x.value,ast.Constant) and isinstance(x.value.value,str))];return node
 def visit_FunctionDef(self,node):
  self.generic_visit(node);node.body=[x for i,x in enumerate(node.body) if not(i==0 and isinstance(x,ast.Expr) and isinstance(x.value,ast.Constant) and isinstance(x.value.value,str))];return node
for i,s in enumerate(x for x in rows if x['target']=='good' and not Path(x['path']).name.startswith('cua-')):
 with zipfile.ZipFile(s['local_path']) as z:
  chunks=[]
  for n in z.namelist():
   if n.endswith('.py'):
    src=z.read(n).decode();tree=ast.parse(src);clean=StripDocs().visit(tree)
    chunks.append(n+'\n'+ast.unparse(clean))
   elif n.endswith('METADATA'):chunks.append(z.read(n).decode())
  out='\n\n'.join(chunks);p=Path('/tmp/endpoint-review-20261023')/('wheel-%02d.txt'%i);p.write_text(s['sha256']+' '+Path(s['path']).name+'\n'+out)
 print(i,Path(s['path']).name,len(out))
