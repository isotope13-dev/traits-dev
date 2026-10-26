"""Apply the reviewed decisions after validation; dry-run by default."""
import argparse,collections,hashlib,json,subprocess
from pathlib import Path
root=Path(__file__).parent;rows=json.load(open(root/'audit.json'))['records'];assert len(rows)==98
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
for target in ('good','bad','purgatory'):
 group=[x for x in rows if x['target']==target]
 for x in group:
  f=Path(x['path']);assert f.is_file();assert hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256']
 cmd=['hopper','mv','-target',target]+([] if a.apply else ['-dry-run'])+[x['sha256'] for x in group]
 r=subprocess.run(cmd,capture_output=True,text=True);(root/f'hopper-{target}-{"applied" if a.apply else "dryrun"}.log').write_text(r.stdout+'\n'+r.stderr)
 print(target,len(group),r.returncode, '\n'.join((r.stdout+'\n'+r.stderr).splitlines()[-4:]),flush=True)
 if r.returncode:raise SystemExit(r.returncode)
