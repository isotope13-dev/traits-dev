"""Scan inert resource references; never execute the examples."""
from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'cleave/target/release/cleave'
rules=['micro-behaviors/fs/path/token::serviceaccount-token-path',
       'micro-behaviors/fs/path/certificate::serviceaccount-ca',
       'micro-behaviors/fs/path/config/environment::serviceaccount-namespace',
       'objectives/credential-access/cloud/token/files::kubernetes-serviceaccount-abuse']
for p in sorted(x for x in here.glob('*.py') if x.name!='check.py'):
 expected=[p.stem in {'token','projected'},p.stem=='ca',p.stem=='namespace',p.stem in {'token','projected'}]
 r=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(p)],text=True,capture_output=True,check=True)
 for rule,yes in zip(rules,expected):
  prefix=('MATCHED ' if yes else 'NOT MATCHED ')+rule+' ('
  assert any(x.startswith(prefix) for x in r.stdout.splitlines()),r.stdout+r.stderr
 print(p.name+': four verdicts verified',flush=True)
