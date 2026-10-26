"""Static lookup reduction; only three reviewed decoders and table rotation run.
The application IIFE is never evaluated. QuickJS has no host callbacks.
"""
from pathlib import Path
from tree_sitter import Language,Parser
import tree_sitter_javascript as tsjs
import quickjs,json,math
base=Path('/tmp/qa2-deep-review');p=next((base/'rfq').rglob('*.js'));src=p.read_bytes();lang=Language(tsjs.language());parser=Parser(lang);tree=parser.parse(src);root=tree.root_node;assert not root.has_error
text=lambda n:src[n.start_byte:n.end_byte].decode()
expr=root.named_children[2].named_children[0]
while expr.type=='parenthesized_expression':expr=expr.named_children[0]
print('top expression',expr.type,[(n.type,n.start_byte,n.end_byte) for n in expr.named_children])
rotation=expr.named_children[0]
assert rotation.type=='call_expression'
bootstrap='\n'.join(text(n) for n in [root.named_children[0],root.named_children[1],root.named_children[-1]])+'\n('+text(rotation)+');'
(base/'reviewed-string-decoder.js').write_text(bootstrap)
ctx=quickjs.Context();ctx.set_memory_limit(128*1024*1024);ctx.set_max_stack_size(2*1024*1024);ctx.set_time_limit(3)
ctx.eval(bootstrap);print('table entries',ctx.eval('Z().length'))
(base/'rotated-string-table.json').write_text(ctx.eval('JSON.stringify(Z())')+'\n')
class Unknown(Exception):pass
class Scope:
 def __init__(self,parent=None):self.parent=parent;self.binds={};self.funcs={}
 def find(self,name):
  if name in self.binds:return self.binds[name],self
  if name in self.funcs:return self.funcs[name],self
  if self.parent:return self.parent.find(name)
  raise Unknown(name)
class Function:
 def __init__(self,node,scope,closure):self.node=node;self.scope=scope;self.closure=closure;self.params=[text(c) for c in node.child_by_field_name('parameters').named_children];self.body=node.child_by_field_name('body')
global_scope=Scope();scope_for={};functions=[];function_by_node={}
class LazyObject:
 def __init__(self,node,scope,env):self.node=node;self.scope=scope;self.env=env
def visit(node,scope):
 scope_for[node.id]=scope
 if node.type in ('function_declaration','function_expression','arrow_function'):
  child=Scope(scope);f=Function(node,child,scope);functions.append(f);function_by_node[node.id]=f
  if node.type=='function_declaration':scope.funcs[text(node.child_by_field_name('name'))]=f
  for c in node.named_children:visit(c,child)
  return
 if node.type=='variable_declarator':
  name=node.child_by_field_name('name');value=node.child_by_field_name('value')
  if name and name.type=='identifier' and value:
   key=text(name)
   if key in scope.binds:scope.binds[key]=None
   else:scope.binds[key]=value
 for c in node.named_children:visit(c,scope)
visit(root,global_scope)
# Runtime decoders are special: their internal mutable cache state is handled
# only by the reviewed, bounded JS implementation.
def lookup(name,scope,env,depth):
 if name in env:return env[name]
 if name in ('w','B') and scope is global_scope:return ('decoder',name)
 val,where=scope.find(name)
 if isinstance(val,Function):
  if where is global_scope and name in ('w','B'):return ('decoder',name)
  return val
 if val is None:raise Unknown('rebound '+name)
 return evaluate(val,where,env,depth+1)
def call(f,args,env,depth):
 if isinstance(f,tuple) and f[0]=='decoder':
  if len(args)<1 or not all(isinstance(x,(str,int,float)) for x in args):raise Unknown('dynamic decode args')
  try:return ctx.eval(f[1]+'('+','.join(json.dumps(v) for v in args)+')')
  except Exception as e:raise Unknown('decode '+str(e))
 if not isinstance(f,Function):raise Unknown('not pure helper')
 stmts=f.body.named_children
 if len(stmts)!=1 or stmts[0].type!='return_statement':raise Unknown('nontrivial function')
 local={**env,**dict(zip(f.params,args))}
 return evaluate(stmts[0].named_children[0],f.scope,local,depth+1)
def evaluate(n,scope,env,depth=0):
 if depth>50:raise Unknown('depth')
 typ=n.type;s=text(n)
 if typ=='number':
  try:return int(s,0)
  except:return float(s)
 if typ=='string':return ctx.eval(s)
 if typ in ['true','false']:return typ=='true'
 if typ=='null':return None
 if typ=='identifier':return lookup(s,scope,env,depth)
 if typ=='parenthesized_expression':return evaluate(n.named_children[0],scope,env,depth+1)
 if typ=='object':return LazyObject(n,scope,env)
 if typ in ('function_expression','arrow_function'):return function_by_node[n.id]
 if typ=='array':return [evaluate(c,scope,env,depth+1) for c in n.named_children]
 if typ in ['member_expression','subscript_expression']:
  obj=evaluate(n.child_by_field_name('object'),scope,env,depth+1)
  key=n.child_by_field_name('property') if typ=='member_expression' else n.child_by_field_name('index')
  key=text(key) if typ=='member_expression' else evaluate(key,scope,env,depth+1)
  if isinstance(obj,LazyObject):
   for pair in obj.node.named_children:
    if pair.type!='pair':continue
    k=pair.child_by_field_name('key');v=pair.child_by_field_name('value');candidate=evaluate(k,obj.scope,obj.env,depth+1) if k.type=='string' else text(k)
    if candidate==key:return evaluate(v,obj.scope,obj.env,depth+1)
   raise Unknown('unknown object key '+str(key))
  if not isinstance(obj,dict) or key not in obj:raise Unknown('dynamic member')
  return obj[key]
 if typ=='unary_expression':
  op=text(n.child_by_field_name('operator'));v=evaluate(n.child_by_field_name('argument'),scope,env,depth+1)
  if op=='-':return -float(v) if isinstance(v,str) and not v.lower().startswith('0x') else -int(v,0) if isinstance(v,str) else -v
  if op=='+':return float(v) if isinstance(v,str) else v
  if op=='!':return False if isinstance(v,(LazyObject,Function,list,dict)) else not v
  if op=='~':return ~int(v)
 if typ=='binary_expression':
  a=evaluate(n.child_by_field_name('left'),scope,env,depth+1);b=evaluate(n.child_by_field_name('right'),scope,env,depth+1);op=text(n.child_by_field_name('operator'))
  if op=='+':return str(a)+str(b) if isinstance(a,str) or isinstance(b,str) else a+b
  if isinstance(a,str):a=int(a,0) if a.lower().startswith('0x') else float(a)
  if isinstance(b,str):b=int(b,0) if b.lower().startswith('0x') else float(b)
  if op=='-':return a-b
  if op=='*':return a*b
  if op=='/':return a/b
  if op=='%':return a%b
  if op=='<<':return int(a)<<int(b)
  if op=='>>':return int(a)>>int(b)
  if op=='^':return int(a)^int(b)
 if typ=='call_expression':
  f=evaluate(n.child_by_field_name('function'),scope,env,depth+1);args=[evaluate(c,scope,env,depth+1) for c in n.child_by_field_name('arguments').named_children];return call(f,args,env,depth+1)
 raise Unknown(typ)
replacements=[];stats={};unknown={}
def collect(n):
 if n.type=='call_expression':
  try:
   fn=n.child_by_field_name('function');f=evaluate(fn,scope_for[n.id],{},0)
   if isinstance(f,Function) or isinstance(f,tuple):
    v=evaluate(n,scope_for[n.id],{},0)
    if isinstance(v,str):
     replacements.append((n.start_byte,n.end_byte,json.dumps(v,ensure_ascii=True).encode(),v));return
  except (Unknown,TypeError,ValueError,KeyError,ZeroDivisionError,OverflowError) as e:unknown[str(e)]=unknown.get(str(e),0)+1
 for c in n.named_children:collect(c)
collect(root)
result=src
for start,end,data,value in sorted(replacements,reverse=True):result=result[:start]+data+result[end:]
(base/'rfq-static-lookups.js').write_bytes(result)
(base/'lookup-reductions.json').write_text(json.dumps([{'start':a,'end':b,'value':v} for a,b,d,v in replacements],indent=2)+'\n')
print('pure functions',len(functions),'lookup replacements',len(replacements),'unknown reasons',sorted(unknown.items(),key=lambda x:-x[1])[:12])
