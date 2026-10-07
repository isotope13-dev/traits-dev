import json, os, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parent.parent
env=os.environ.copy()
for key in ['CLEAVE_VALIDATE','SCAN_HOPPER','SCAN_FETCH']:env.pop(key,None)
env['CLEAVE_TRAITS_DIR']=str(repo)
for case in json.loads((root/'cases.json').read_text()):
 result=subprocess.run(['atomscan','--no-update','--follow=none','--mode','slow','-f','json',str(root/case['file'])],env=env,capture_output=True,text=True)
 try:ids={t['id'] for f in json.loads(result.stdout)['raw']['files'] for t in f.get('traits',[])}
 except Exception:raise RuntimeError(result.stderr)
 missing=set(case['present'])-ids
 unwanted=set(case['absent'])&ids
 assert not missing and not unwanted,(case['file'],missing,unwanted)
 print('PASS',case['file'],flush=True)
