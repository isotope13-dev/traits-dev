"""Scan inert path examples without executing them."""
from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'cleave/target/release/cleave'
rules=['micro-behaviors/fs/path/token::serviceaccount-token',
       'micro-behaviors/fs/path/token::projected-serviceaccount-token',
       'micro-behaviors/fs/path/token::serviceaccount-token-path']
for p in sorted(here.glob('*.js')):
 expected=[p.stem=='default',p.stem in {'default','projected'},p.stem in {'default','projected'}]
 r=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(p)],text=True,capture_output=True,check=True)
 for rule,yes in zip(rules,expected):
  prefix=('MATCHED ' if yes else 'NOT MATCHED ')+rule+' ('
  assert any(x.startswith(prefix) for x in r.stdout.splitlines()),r.stdout+r.stderr
 print(p.name+': three verdicts verified',flush=True)
