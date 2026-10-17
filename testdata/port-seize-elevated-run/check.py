import json, os, re, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parent.parent
env=os.environ.copy()
for key in ['CLEAVE_VALIDATE','SCAN_HOPPER','SCAN_FETCH']:env.pop(key,None)
env['CLEAVE_TRAITS_DIR']=str(repo)
cases=json.loads((root/'cases.json').read_text())
result=subprocess.run(['atomscan','--no-update','--follow=none','--mode','slow','-f','json',*[str(root/case['file']) for case in cases if not case.get('inspect_baseline')]],env=env,capture_output=True,text=True)
try:reports=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
except Exception:raise RuntimeError(result.stderr)
by_path={str(Path(report['raw']['files'][0]['path']).resolve()):report for report in reports}
for case in cases:
 if case.get('inspect_baseline'):
  ids_to_test=case['present']+case['absent']
  traced=subprocess.run(['cleave','test-rules','--rules',','.join(ids_to_test),str(root/case['file'])],env=env,capture_output=True,text=True)
  assert traced.returncode==0,traced.stderr
  ids=set(re.findall(r'^MATCHED (\S+)',traced.stdout,re.M))
 else:
  report=by_path[str(root/case['file'])]
  ids={t['id'] for f in report['raw']['files'] for t in f.get('traits',[])}
 missing=set(case['present'])-ids
 unwanted=set(case['absent'])&ids
 assert not missing and not unwanted,(case['file'],missing,unwanted)
 print('PASS',case['file'],flush=True)
