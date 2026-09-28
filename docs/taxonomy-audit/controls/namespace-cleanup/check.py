"""Scan inert term/operation examples; never execute them."""
from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'cleave/target/release/cleave'
rules=['metadata/file/string/container::runc-refs',
       'metadata/file/string/container::oci',
       'metadata/file/string/container::cni-refs',
       'micro-behaviors/os/network/interface::veth-str',
       'micro-behaviors/os/container/namespace::user-network-namespace-command',
       'micro-behaviors/os/container/namespace::ns-refs',
       'micro-behaviors/os/container/namespace::setns-str',
       'micro-behaviors/fs/directory/root::host-root-chroot']
for p in sorted(here.glob('*.py')):
 if p.name=='check.py':continue
 expected=[p.stem=='terms',p.stem=='terms',p.stem=='terms',p.stem=='terms',
           p.stem=='operations',p.stem=='operations',p.stem=='operations',p.stem=='operations']
 r=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(p)],text=True,capture_output=True,check=True)
 for rule,yes in zip(rules,expected):
  prefix=('MATCHED ' if yes else 'NOT MATCHED ')+rule+' ('
  assert any(x.startswith(prefix) for x in r.stdout.splitlines()),r.stdout+r.stderr
 print(p.name+': eight verdicts verified',flush=True)
