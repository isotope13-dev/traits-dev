#!/usr/bin/env python3
"""Static regression controls. Fixture code is parsed, never executed."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
raw='objectives/credential-access/capture/input::android-raw-touch-credential-reconstruction'
flow='objectives/credential-access/capture/input::android-adb-input-to-credential-mapping'
implant='objectives/command-and-control/backdoor/rat/remote-agent::android-adb-accessibility-input-implant'
bypass='objectives/privilege-escalation/elevation-control/permission::android-remote-adb-accessibility-grant'
c2='objectives/command-and-control/remote-command/control/adb::android-wireless-adb-c2-shell'
tg='objectives/command-and-control/remote-command/tasking::telegram-document-task-launch-loop'
watchdog='micro-behaviors/process/enumerate/shell::powershell-process-query-empty-check'
cases=[
 ('process-liveness.ps1',[watchdog],[]),
 ('process-query-only.ps1',[],[watchdog]),
 ('android-provisioning-example.java',[],[raw,flow,implant,bypass,c2]),
 ('android-remote-input-agent.java',[implant,bypass,c2],[raw,flow]),
 ('android-raw-credential-flow.java',[raw,flow],[implant,bypass,c2]),
 ('android-unrelated-credential-flow.java',[],[raw,flow,implant,bypass,c2]),
 ('telegram-concealed-task.ps1',[tg],[]),
 ('telegram-document-download-only.ps1',[],[tg]),
 ('telegram-different-launch-path.ps1',[],[tg]),
 ('telegram-visible-launch.ps1',[],[tg]),
]
# Existing positive/negative fixtures outside this batch retain their assertions.
for directory in ['testdata/taxonomy/credential-overlay-review','testdata/taxonomy/powershell-masked-native-host']:
 data=json.loads((ROOT/directory/'cases.json').read_text())
 for case in data['fixtures']:
  cases.append((str(ROOT/case['path']),case['matched'],case['not_matched']))
if __name__=='__main__':
 paths=[Path(n) if Path(n).is_absolute() else HERE/n for n,_,_ in cases]
 result=subprocess.run(['cleave','--traits-dir',str(ROOT),'--format','jsonl',*map(str,paths)],text=True,capture_output=True,timeout=600,check=True)
 assert not result.stderr.strip(),result.stderr
 reports=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
 files={str(Path(f['path']).resolve()):f for r in reports for f in r['files']}
 for path,(_,yes,no) in zip(paths,cases):
  file=files[str(path.resolve())]
  matched={t['id'] for t in file.get('traits',[])}
  assert set(yes)<=matched and not set(no)&matched,(path.name,'missing',set(yes)-matched,'unexpected',set(no)&matched)
  print('PASS',path.name,flush=True)
 print(f'{len(cases)} static coverage checks passed',flush=True)
