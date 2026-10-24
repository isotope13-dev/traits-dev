from pathlib import Path
import ast,json,types
p=next(Path('/tmp/qa2/hostile').glob('7e916*/setup.py'));source=p.read_text();results=[]
for corrected in [False,True]:
 tree=ast.parse(source.replace('urllib.urlrequest','urllib.request') if corrected else source);trial=next(n for n in tree.body if isinstance(n,ast.Try));events=[]
 def retrieve(url,path):events.append({'operation':'urlretrieve','url':url,'path':path})
 def run(args,**kw):events.append({'operation':'run','argv':args,'kwargs':kw})
 def display(error):events.append({'operation':'caught-error','message':str(error)})
 ns={'urllib':types.SimpleNamespace(request=types.SimpleNamespace(urlretrieve=retrieve)),'run':run,'print':display,'__builtins__':{'Exception':Exception}}
 exec(compile(ast.Module(body=[trial],type_ignores=[]),'isolated-setup-try.py','exec'),ns)
 assert len(events)==(2 if corrected else 1)
 if corrected:assert events[0]['path']==events[1]['argv'][1]
 else:assert events[0]['operation']=='caught-error' and 'urlrequest' in events[0]['message']
 results.append({'corrected_typo_control':corrected,'events':events})
Path('/tmp/qa2-deep-review/setup-synthetic-replay.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
