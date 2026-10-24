"""Replay only the extracted metrics function with synthetic modules and I/O.
No package imports, real environment reads, subprocesses or network access.
"""
import ast,builtins,hashlib,json,pathlib,re,types
from typing import Optional
sources=[next(pathlib.Path('/var/tmp/qa/hostile').glob('dc*/track_info.py'))]
sources+=list(pathlib.Path('/tmp/hostile-triage').glob('a03*/upgini/utils/track_info.py'))
sources+=list(pathlib.Path('/tmp/hostile-triage').glob('e60*/upgini/utils/track_info.py'))
all_results=[]
for source in sources:
 tree=ast.parse(source.read_text());function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_compute_track_metrics');function.decorator_list=[]
 # Only this reviewed function is compiled. All imported notebook objects are
 # synthetic, and the builtins import hook rejects any other import.
 for ide,success,overrides in [('other',False,False),('other',False,True),('binder',False,False),('binder',False,True),('kaggle',False,False),('kaggle',True,False),('colab',False,False),('colab',False,True)]:
  events=[]
  def get(url,**kwargs):events.append({'kind':'get','url':url,'kwargs':kwargs});return types.SimpleNamespace(text='203.0.113.7')
  class Response:
   def __enter__(self):return self
   def __exit__(self,*args):return False
   def json(self):return {'secret':'SYNTHETIC_SECRET_NEVER_RETURNED'} if success else {'errors':['User 123456789 cannot find label api-key']}
  def post(url,**kwargs):events.append({'kind':'post','url':url,'kwargs':kwargs});return Response()
  def eval_js(code,**kwargs):events.append({'kind':'eval_js','code':code});return 'synthetic-browser-visitor' if 'Visitor' in code else '203.0.113.7'
  output=types.SimpleNamespace(eval_js=eval_js)
  def display(value):events.append({'kind':'display_js','source':value})
  ipy=types.SimpleNamespace(Javascript=lambda x:x,display=display)
  def safe_import(name,globals=None,locals=None,fromlist=(),level=0):
   if name=='google.colab':return types.SimpleNamespace(output=output)
   if name=='IPython.display':return ipy
   raise AssertionError('Unexpected import '+name)
  safe_builtins={name:getattr(builtins,name) for name in ['Exception','str']};safe_builtins['__import__']=safe_import
  env={'CLIENT_IP':'198.51.100.4','KAGGLE_USER_SECRETS_TOKEN':'SYNTHETIC_KAGGLE_TOKEN'}
  fake_os=types.SimpleNamespace(environ=env,getenv=env.get)
  ns={'__builtins__':safe_builtins,'Optional':Optional,'_get_execution_ide':lambda:ide,'socket':types.SimpleNamespace(gethostname=lambda:'synthetic-host'),'getuser':lambda:'synthetic-user','os':fake_os,'getnode':lambda:0x001122334455,'sha256':hashlib.sha256,'get':get,'post':post,'re':re}
  exec(compile(ast.Module(body=[function],type_ignores=[]),str(source),mode='exec'),ns)
  result=ns['_compute_track_metrics']('192.0.2.9' if overrides else None,'override-visitor' if overrides else None)
  assert 'SYNTHETIC_SECRET_NEVER_RETURNED' not in json.dumps(result)
  assert 'SYNTHETIC_KAGGLE_TOKEN' not in json.dumps(result)
  if ide=='kaggle':
   assert len(events)==1 and events[0]['kind']=='post'
   assert events[0]['url']=='https://www.kaggle.com/requests/GetUserSecretByLabelRequest'
   assert result['visitorId']==('None' if success else '123456789')
  if ide=='other' and overrides:assert events==[] and result['visitorId']=='override-visitor'
  if ide=='binder':assert events==[] and result['visitorId']==hashlib.sha256(env['CLIENT_IP'].encode()).hexdigest()
  all_results.append({'source':str(source),'ide':ide,'secret_response_success':success,'caller_overrides':overrides,'result':result,'synthetic_events':events})
pathlib.Path('/tmp/purgatory-reverse-review/tracker-replay.json').write_text(json.dumps(all_results,indent=2)+'\n')
print(len(all_results),'isolated tracker branch replays passed')
