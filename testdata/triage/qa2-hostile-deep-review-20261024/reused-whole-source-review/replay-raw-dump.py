"""Replay only the extracted raw-frame dumping method with virtual I/O.
Every frame, path, thread, hash, logger and client is synthetic.
"""
import ast,contextlib,hashlib,json,pathlib,types
results=[]
for source in pathlib.Path('/tmp/hostile-triage').glob('*/upgini/features_enricher.py'):
 if not source.parts[3].startswith(('a03','e60')):continue
 tree=ast.parse(source.read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='FeaturesEnricher');fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='dump_input')
 assert not any(isinstance(n,ast.Attribute) and n.attr=='logs_enabled' for n in ast.walk(fn))
 # Confirm the callers pass original variables, before inner enrichment.
 caller_evidence=[]
 for caller in cls.body:
  if not isinstance(caller,ast.FunctionDef) or caller.name not in ['fit','fit_transform','transform']:continue
  calls=sorted([n for n in ast.walk(caller) if isinstance(n,ast.Call)],key=lambda n:(n.lineno,n.col_offset))
  dump=next(n for n in calls if ast.unparse(n.func)=='self.dump_input')
  inner=next(n for n in calls if ast.unparse(n.func) in ['self.__inner_fit','self.__inner_transform'])
  assert dump.lineno<inner.lineno
  assert isinstance(dump.args[0],ast.Name) and dump.args[0].id=='X'
  caller_evidence.append({'caller':caller.name,'dump_line':dump.lineno,'processing_line':inner.lineno,'call':ast.unparse(dump)})
 assert len(caller_evidence)==3
 for logs_enabled in [False,True]:
  for already_uploaded in [False,True]:
   events=[]
   class Frame:
    def __init__(self,name,columns):self.name=name;self.columns=columns
    def to_parquet(self,path,**kwargs):events.append({'kind':'serialize','frame':self.name,'columns':self.columns,'path':path,'options':kwargs})
   class Series(Frame):
    def to_frame(self):return Frame(self.name,self.columns)
   class Thread:
    def __init__(self,target,args,daemon):self.target=target;self.args=args;assert daemon is True;events.append({'kind':'thread','daemon':daemon})
    def start(self):self.target(*self.args)
   class Client:
    def is_file_uploaded(self,trace,digest):events.append({'kind':'exists','digest':digest});return already_uploaded
    def dump_input_file(self,trace,path,name,digest):events.append({'kind':'upload','name':name,'path':path,'digest':digest})
   class Logger:
    def warning(self,*a,**kw):raise AssertionError('Unexpected warning '+str(a))
    def info(self,*a,**kw):pass
   ns={'pd':types.SimpleNamespace(DataFrame=Frame,Series=Series),'MDC':lambda **kw:contextlib.nullcontext(),'tempfile':types.SimpleNamespace(TemporaryDirectory=lambda:contextlib.nullcontext('/synthetic/tmp')),'Path':lambda p:types.SimpleNamespace(stat=lambda:types.SimpleNamespace(st_size=64)),'Dataset':types.SimpleNamespace(MAX_UPLOADING_FILE_SIZE=536870912),'file_hash':lambda p:hashlib.sha256(p.encode()).hexdigest(),'Thread':Thread}
   # Compiling this single, reviewed method never imports the package.
   exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),'exec'),ns)
   self=types.SimpleNamespace(_get_trace_id=lambda:'synthetic-trace',logs_enabled=logs_enabled,rest_client=Client(),logger=Logger())
   x=Frame('X',['public_feature','private_excluded_column']);y=Series('y',['private_target']);ex=Frame('eval_X',['private_eval']);ey=Series('eval_y',['eval_target'])
   ns['dump_input'](self,x,y,[(ex,ey)])
   assert len([e for e in events if e['kind']=='serialize'])==4
   assert len([e for e in events if e['kind']=='upload'])==(0 if already_uploaded else 4)
   assert events[1]['columns']==x.columns
   results.append({'source':str(source),'logs_enabled':logs_enabled,'already_uploaded':already_uploaded,'caller_evidence':caller_evidence,'events':events})
pathlib.Path('/tmp/purgatory-reverse-review/raw-dump-replay.json').write_text(json.dumps(results,indent=2)+'\n')
print(len(results),'isolated raw-frame upload replays passed')
