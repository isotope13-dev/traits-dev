"""Focused controls for memory-path overclaims and caller-owned OAuth tokens."""
from pathlib import Path
import json,subprocess,os,lzma,tempfile
root=Path(__file__).resolve().parents[3]
base=Path(__file__).resolve().parent
memory='objectives/credential-access/memory::'
reader='micro-behaviors/mem/read/cross-process::python-proc-region-read-to-write'
replay='objectives/credential-access/cloud/token/weaponization::owa-bearer-session-replay'
rewrite='micro-behaviors/communications/http/authorization-header::microsoft-client-request-header-rewrite'
xwiki='objectives/execution/exploit/code-injection::xwiki-groovy-command-http-client'
results=[]
def run(path,required=(),forbidden=(),max_hostile=None):
 cmd=[os.environ.get('CLEAVE','cleave'),'--traits-dir',str(root),'--format','json',str(path)]
 d=json.loads(subprocess.check_output(cmd,text=True));ts=[t for f in d['files'] for t in f.get('traits',[])];ids={t['id'] for t in ts}
 assert set(required)<=ids,(path,'missing',set(required)-ids)
 assert not set(forbidden)&ids,(path,'unexpected',set(forbidden)&ids)
 hostile=sum(t['crit']==5 for t in ts)
 if max_hostile is not None: assert hostile<=max_hostile,(path,hostile)
 results.append({'fixture':str(path.relative_to(root)) if path.is_relative_to(root) else path.name,'hostile':hostile,'checked_required':list(required),'checked_forbidden':list(forbidden)})
 print('PASS',path.name,flush=True)
for name in ['renamed-runner-dump.py','runner-file-output.py']:
 run(base/name,[reader,memory+'proc-memory-cmdline-credential-dump',memory+'proc-enumeration-memory-credential-dump'])
for name in ['runner-paths-only.py','unrelated-read.py','unrelated-output.py']:
 run(base/name,forbidden=[reader,memory+'proc-memory-cmdline-credential-dump',memory+'proc-enumeration-memory-credential-dump'],max_hostile=0)
run(base/'upstream-memory-diagnostic.py',max_hostile=0)
run(base/'own-token-session.js',[replay,rewrite],max_hostile=0)
run(root/'testdata/suspicious/owa-bearer-replay-controls.py',[replay],max_hostile=0)
run(base/'ordinary-search.py',forbidden=[xwiki],max_hostile=0)
run(base/'xwiki-command-request.py',[xwiki])
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'memdump.py';p.write_bytes(lzma.decompress((root/'testdata/hostile/memdump.py.xz').read_bytes()))
 run(p,[reader,memory+'proc-memory-cmdline-credential-dump',memory+'proc-enumeration-memory-credential-dump'])
(base/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
