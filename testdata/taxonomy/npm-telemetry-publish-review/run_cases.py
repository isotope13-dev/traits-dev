#!/usr/bin/env python3
"""Stage fixtures outside test-path suppressors and verify actual rule output."""
import argparse, json, os, shutil, subprocess
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--scratch',required=True)
ap.add_argument('--cleave',default='cleave')
a=ap.parse_args()
base=Path(__file__).parent
cases=json.loads((base/'cases.json').read_text())['fixtures']
stage=Path(a.scratch);stage.mkdir(parents=True,exist_ok=True)
paths=[]
for i,c in enumerate(cases):
 target=stage/str(i)/Path(c['path']).name
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(c['path'],target)
 paths.append(str(target))
env=dict(os.environ,CLEAVE_VALIDATE='0')
r=subprocess.run([a.cleave,'--traits-dir','.', '--format','json',*paths],env=env,text=True,capture_output=True)
if r.returncode: raise SystemExit(r.stderr)
(stage/'reports.json').write_text(r.stdout)
dec=json.JSONDecoder();text=r.stdout;files=[]
while text.strip():
 d,end=dec.raw_decode(text.lstrip());text=text.lstrip()[end:]
 files.extend(d.get('files',[]))
by_path={f['path']:{t['id'] for t in f.get('traits',[])} for f in files}
fail=[]
for c,path in zip(cases,paths):
 got=by_path.get(path,set())
 fail.extend(c['path']+': missing '+t for t in c['matched'] if t not in got)
 fail.extend(c['path']+': unexpected '+t for t in c['not_matched'] if t in got)
# Component observations are retained by the evaluator but stripped from
# ordinary reports without a surviving consumer. Test their actual matcher
# directly; never inflate severity to make them visible.
for i,(c,path) in enumerate(zip(cases,paths)):
 for match in c.get('atomic_matches',[]):
  rules=stage/'atomic-rules'/str(i);rules.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(match['yaml'],rules/Path(match['yaml']).name)
  probe=subprocess.run([a.cleave,'--traits-dir',str(rules),'test-rules',path,'--rules',match['id']],env=env,text=True,capture_output=True)
  (stage/(str(i)+'.atomic.txt')).write_text(probe.stdout+probe.stderr)
  observed=('\nMATCHED '+match['id']+' ') in probe.stdout
  if probe.returncode or observed!=match['matched']:fail.append(c['path']+': atomic matcher mismatch '+match['id'])
result={'cases':len(cases),'failures':fail}
(stage/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(fail))
