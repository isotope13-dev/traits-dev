#!/usr/bin/env python3
"""Check shared-rule precision and retained coverage outside test path exclusions."""
import argparse, json, pathlib, shutil, subprocess
p=argparse.ArgumentParser()
p.add_argument('--scratch',required=True)
p.add_argument('--baseline')
a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[3]
fixtures=pathlib.Path(__file__).resolve().parent
scratch=pathlib.Path(a.scratch).resolve()
controls=scratch/'controls'
controls.mkdir(parents=True,exist_ok=True)
cases=json.loads((fixtures/'cases.json').read_text())
for c in cases:shutil.copyfile(fixtures/c['file'],controls/c['file'])
# Existing controls outside this batch, copied to avoid test-directory exclusions.
existing=[('testdata/sysvol-inline-copy/positive.cmd','sysvol-positive.cmd','micro-behaviors/fs/file/copy::sysvol-script-file-transfer'),('testdata/taxonomy/sysvol-public-launch/privileged-tunnel.cmd','tunnel-positive.cmd','objectives/command-and-control/channel/tunnel/relay::privileged-sysvol-execution-and-tunnel-service')]
for src,dst,trait in existing:
 shutil.copyfile(root/src,controls/dst)
 cases.append(dict(file=dst,present=[trait],absent=[]))
shutil.copyfile(root/'testdata/benign/sysvol-backup.cmd',controls/'sysvol-backup.cmd')
cases.append(dict(file='sysvol-backup.cmd',present=['micro-behaviors/fs/file/copy::sysvol-script-file-transfer'],absent=['objectives/lateral-movement/smb::defender-suppressed-sysvol-remote-execution']))
results={}
for label,traits_dir in [('after',root)]+([('before',pathlib.Path(a.baseline))] if a.baseline else []):
 cmd=['cleave','--traits-dir',str(traits_dir),'--json',str(controls)]
 run=subprocess.run(cmd,capture_output=True,text=True,check=True)
 (scratch/(label+'-controls.json')).write_text(run.stdout)
 (scratch/(label+'-controls.err')).write_text(run.stderr)
 documents=[json.loads(line) for line in run.stdout.splitlines() if line.strip()]
 reports={pathlib.Path(f['path']).name:f for d in documents for f in d.get('files',[])}
 checks=[]
 for c in cases:
  report=reports[c['file']]; found={t['id']:t['crit'] for t in report.get('traits',[])}
  present=c.get('present',[]) if label=='after' else c.get('old_present',[])
  absent=c.get('absent',[]) if label=='after' else []
  missing=[t for t in present if t not in found]
  unexpected=[t for t in absent if t in found]
  checks.append(dict(file=c['file'],missing=missing,unexpected=unexpected,hostile=sum(x==5 for x in found.values()),suspicious=sum(x==4 for x in found.values())))
  if missing or unexpected:print(label,c['file'],'missing',missing,'unexpected',unexpected)
 results[label]=checks
(scratch/'control-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert not any(c['missing'] or c['unexpected'] for checks in results.values() for c in checks), 'control failures'
print(f'{len(cases)} controls passed'+(' before and after' if a.baseline else ''))
