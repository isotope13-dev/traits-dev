from pathlib import Path
import json,hashlib,subprocess,re
root=Path('/home/t/src/traits-dev/testdata/triage/hopper-new-evidence-20261023');out=root/'deep-review';d=json.load(open(out/'review-final.json'));audit=[]
changed=[s for s in d['samples'] if 'previous_label' in s]
assert len(changed)==8
for s in changed:
 p=Path(s.get('relocated_local_path',s['path']));assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
for s in changed:
 cmd=['hopper','mv','-target',s['label'],s['sha256']];r=subprocess.run(cmd,capture_output=True,text=True);m=re.search(r'Summary: (\d+) moved, (\d+) noop, (\d+) absent, (\d+) failed',r.stdout);counts=dict(zip(['moved','noop','absent','failed'],map(int,m.groups()))) if m else {};row={'sha256':s['sha256'],'previous_label':s['previous_label'],'target':s['label'],'command':cmd,'returncode':r.returncode,'counts':counts,'stdout':r.stdout,'stderr':r.stderr};audit.append(row);(out/'hopper-actions.json').write_text(json.dumps(audit,indent=2)+'\n');assert r.returncode==0 and counts and counts['absent']==0 and counts['failed']==0,row;s['hopper_action']=counts;print(s['sha256'][:12],s['label'],counts,flush=True)
 if s['label']=='good' and 'relocated_local_path' not in s:
  p=Path(s['path']);dest=Path('/tmp/triage/misplaced-good/hopper-new-evidence-20261023')/p.relative_to('/var/tmp/hopper-triage/new');assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);subprocess.run(['mv','--',str(p),str(dest)],check=True);assert hashlib.sha256(dest.read_bytes()).hexdigest()==s['sha256'];s['relocated_local_path']=str(dest)
 (out/'review-final.json').write_text(json.dumps(d,indent=2)+'\n')
 (root/'review.json').write_text(json.dumps(d,indent=2)+'\n')
print('Updated all eight formerly unresolved labels and verified the newly benign local move.')
