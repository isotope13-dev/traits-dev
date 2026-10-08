#!/usr/bin/env python3
"""Check positive evidence and near misses; never execute specimen code."""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--cleave',default='../cleave/target/release/cleave');args=p.parse_args()
root=Path(__file__).resolve().parents[3];cases=json.loads(Path(__file__).with_name('cases.json').read_text())['cases']
result=subprocess.run([args.cleave,'--no-update-check','--traits-dir','.', '--format=json',*[c['path']for c in cases]],cwd=root,check=True,capture_output=True,text=True)
dec=json.JSONDecoder();pending=result.stdout;reports={}
while pending.strip():
 report,end=dec.raw_decode(pending.lstrip());pending=pending.lstrip()[end:]
 for f in report['files']:reports[Path(f['path']).name]=f
failed=[]
for c in cases:
 f=reports[c['name']];ids={t['id']for t in f.get('traits',[])}
 for trait in c['required_traits']:
  if trait not in ids:failed.append(f"{c['name']}: missing {trait}")
 for trait in c['forbidden_traits']:
  if trait in ids:failed.append(f"{c['name']}: unexpected {trait}")
 if any(t['crit']>=5 for t in f.get('traits',[])):failed.append(f"{c['name']}: unsupported hostile verdict")
if failed:raise SystemExit('\n'.join(failed))
print(f'{len(cases)} audit triage controls passed')
