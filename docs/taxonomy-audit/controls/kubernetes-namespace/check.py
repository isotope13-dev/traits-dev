"""Scan inert reference examples without executing them."""
from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'cleave/target/release/cleave'
rules=['micro-behaviors/communications/http/services/kubernetes::apps-v1-path-text',
       'micro-behaviors/communications/http/services/kubernetes::pods-v1-path-text',
       'micro-behaviors/os/env/config::kubeconfig-name',
       'micro-behaviors/os/container/namespace::clone-newnet-str',
       'objectives/credential-access/env/secrets/bulk-access::script-cross-vendor-secret-catalog-harvest']
for p in sorted(x for x in here.glob('*.py') if x.name!='check.py'):
 expected=[p.stem=='apps',p.stem=='pods',p.stem in {'config','catalog-names','catalog-read'},p.stem=='namespace',p.stem=='catalog-read']
 r=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(p)],text=True,capture_output=True,check=True)
 for rule,yes in zip(rules,expected):
  prefix=('MATCHED ' if yes else 'NOT MATCHED ')+rule+' ('
  assert any(x.startswith(prefix) for x in r.stdout.splitlines()),r.stdout+r.stderr
 print(p.name+': five verdicts verified',flush=True)
