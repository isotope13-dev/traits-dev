"""Scan inert Go/Python examples; never build or execute them."""
from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'cleave/target/release/cleave'
rules=['micro-behaviors/fs/path/credential::kubernetes-secret-directory-text',
       'micro-behaviors/fs/path/credential::kubernetes-secret-directory-literal',
       'micro-behaviors/os/container/runtime::kubernetes-package-imports']
for p in sorted(x for x in here.iterdir() if x.suffix in {'.go','.py'} and x.name!='check.py'):
 expected=[p.name=='path.py',p.name=='path.go',p.name=='import.go']
 r=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(p)],text=True,capture_output=True,check=True)
 for rule,yes in zip(rules,expected):
  prefix=('MATCHED ' if yes else 'NOT MATCHED ')+rule+' ('
  assert any(x.startswith(prefix) for x in r.stdout.splitlines()),r.stdout+r.stderr
 print(p.name+': three verdicts verified',flush=True)
