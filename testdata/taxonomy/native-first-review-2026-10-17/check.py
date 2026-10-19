"""Run focused controls against the current trait tree."""
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).parent
layout='metadata/binary/instruction/sequence::x64-sized-buffer-call-forward-layout'
report='micro-behaviors/communications/http/request/body::native-sensitive-path-report-context'
resource='micro-behaviors/fs/write/file/resource::drive-exe-search-resource-edit-api-set'
mac='micro-behaviors/communications/http/message::urlencoded-mac-address-field'
ssh='micro-behaviors/communications/ssh/client::ssh-command-history-reference'
retired={
 'objectives/collection/multi-source::native-screen-keyboard-clipboard-run-key-spyware',
 'objectives/impact/infect/resource::delphi-resource-appender',
 'objectives/lateral-movement/infection/file::pe-resource-drive-infector',
 'objectives/lateral-movement/ssh/connect::ssh-shell-history',
 'micro-behaviors/communications/http/telemetry::hardware-address-report-parameter',
}
cases={
 'buffer-path-post.elf':({layout,report},set()),
 'paths-post-only.elf':(set(),{layout,report}),
 'buffer-post-only.elf':({layout},{report}),
 'buffer-path-only.elf':({layout},{report}),
 'different-buffer.elf':(set(),{layout,report}),
 'gui-resource-editor.exe':({resource},set()),
 'router-form.sh':({mac},set()),
 'history-command.sh':({ssh},set()),
 'history-pattern.sh':(set(),{ssh}),
}
r=subprocess.run(['atomscan','--follow=none','--format=json',*[str(ROOT/n) for n in cases]],capture_output=True,text=True)
assert r.returncode in (0,1),(r.returncode,r.stderr)
seen=set()
for line in r.stdout.splitlines():
 d=json.loads(line)
 for f in d['raw']['files']:
  name=Path(f['path']).name
  if name not in cases:continue
  seen.add(name);ts={t['id']:t for t in f.get('traits',[])}
  present,absent=cases[name]
  assert present<=ts.keys(),(name,'missing',present-ts.keys())
  assert not (absent|retired)&ts.keys(),(name,'unexpected',(absent|retired)&ts.keys())
  assert not [t['id'] for t in ts.values() if t['crit']==5],(name,'hostile finding on inert control')
assert seen==cases.keys(),('unscanned controls',cases.keys()-seen,r.stderr)
print(f'{len(seen)} controls passed')
