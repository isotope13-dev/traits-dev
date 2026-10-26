#!/usr/bin/env python3
"""Static regression controls; never execute specimen code.

Usage: python3 verify.py SAMPLES_ROOT SCRATCH_DIRECTORY
Requires dnfile and cleave. Original artifacts remain outside the checkout.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import dnfile

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
MODULE = 'micro-behaviors/process/interpreter/runtime/clr::cil-input-assembly-module-instantiation'
CLIP = 'micro-behaviors/os/clipboard/read::managed-clipboard-handle-string-read'
CLIP_COLLECTION = 'objectives/collection/clipboard/capture::managed-ransom-keylogger-clipboard-read-append'
HTTP = 'micro-behaviors/communications/http/client/managed::httpclient-get-temp-launch-references'
OLD_HTTP = 'objectives/command-and-control/dropper/file-exec/spawn::dotnet-httpclient-temp-execute-dropper'
OBF = 'objectives/anti-static/obfuscation/string/concat::ps-obfuscated-eval'
NEW_PERSIST = {
 'objectives/credential-access/credential-manager/store-api::managed-keylogger-credential-directory-copy-references',
 'objectives/persistence/login/startup/folder::managed-keylogger-startup-batch-profile',
 'objectives/persistence/login/scheduled-task/cli::managed-keylogger-logon-task',
}
PS = SAMPLES / '579c2a9e81ad' / 'cleaner-representative.ps1'
RAT = next((SAMPLES / '2bc04f26c8ca').glob('*.exe'))
RANSOM = SAMPLES / '58809df1c731' / 'xoilac66-tv.online_hyber.exe'
for p,h in [(PS,'579c2a9e81ad201665e89a81c661cac498d84cc95307b12a6ebab0048c96ddd1'),
 (RAT,'2bc04f26c8caabe5cfa08a6deaf2fb564ebb0d9c76e5347091d6be7514e87cd9'),
 (RANSOM,'58809df1c731a8252eccf608ddfd71c512a3a3587e4c1159dcbd5b0edd0c246d')]:
 assert hashlib.sha256(p.read_bytes()).hexdigest() == h


def scan(path):
 p = subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--format','json',str(path)],capture_output=True,text=True)
 assert p.returncode == 0, (str(path),p.stderr)
 assert not p.stderr.strip(), p.stderr
 d = json.loads(p.stdout)
 (OUT / (path.name+'.scan.json')).write_text(json.dumps(d,indent=2))
 return {t['id']:t for f in d['files'] for t in f.get('traits',[])}


rat_data = RAT.read_bytes()
ransom_data = RANSOM.read_bytes()
# Inert byte mutations test required code and API clues independently. They
# are structural near misses, not claims about runnable benign programs.
mutations = []
for name,base,method,offset,before,after in [
 ('module-without-load-call.exe',rat_data,0x46,0x0d,b'\x28',b'\x00'),
 ('clipboard-without-conversion-call.exe',ransom_data,0x85,0x91,b'\x28',b'\x00'),
]:
 pe=dnfile.dnPE(data=base)
 pos=pe.get_offset_from_rva(pe.net.mdtables.MethodDef.rows[method-1].Rva)+offset
 assert base[pos:pos+len(before)]==before
 p=OUT/name;p.write_bytes(base[:pos]+after+base[pos+len(before):]);mutations.append(p)
for name,base,before,after in [
 ('module-without-module-api.exe',rat_data,b'GetModules\0',b'GetObjects\0'),
 ('clipboard-without-string-api.exe',ransom_data,b'PtrToStringUni\0',b'PtrToStringAn1\0'),
]:
 assert before in base and len(before)==len(after)
 p=OUT/name;p.write_bytes(base.replace(before,after));mutations.append(p)
benign_ps=OUT/'numeric-message.ps1'
message="Write-Output 'Maintenance complete'"
benign_ps.write_text('IEX (-join [char[]]@('+','.join(hex(ord(c)) for c in message)+'))\n')
paths=[PS,RAT,RANSOM,*mutations,benign_ps,
 ROOT/'testdata/benign/dotnet-normal-loader-controls.exe',
 ROOT/'testdata/benign/keylog-dropper-controls.exe',
 ROOT/'testdata/hostile/xworm-v3-obfuscated-client.exe',
 ROOT/'testdata/hostile/ps-cradle-stager.ps1',
 ROOT/'testdata/triage/registry-second-review-607680-0906-8175/controls/keylog-unrelated-reply.exe',
 *sorted((ROOT/'testdata/taxonomy/powershell-char-array-join').glob('*.ps1'))]
with ThreadPoolExecutor(max_workers=3) as pool:
 reports=dict(zip(paths,pool.map(scan,paths)))
assert reports[PS][OBF]['crit']==4
assert not any(t['crit']==5 for t in reports[PS].values())
assert reports[benign_ps][OBF]['crit']==4
assert not any(t['crit']==5 for t in reports[benign_ps].values())
assert MODULE in reports[RAT] and CLIP not in reports[RAT]
assert sum(t['crit']==5 for t in reports[RAT].values())==6
assert NEW_PERSIST <= reports[RANSOM].keys()
assert CLIP in reports[RANSOM] and CLIP_COLLECTION in reports[RANSOM]
assert HTTP in reports[RANSOM] and OLD_HTTP not in reports[RANSOM]
assert sum(t['crit']==5 for t in reports[RANSOM].values())==22
for p in mutations:
 if p.name.startswith('module-'):assert MODULE not in reports[p]
 else:assert CLIP not in reports[p] and CLIP_COLLECTION not in reports[p]
for p in paths:
 if p.parent==ROOT/'testdata/benign':assert not ({MODULE,CLIP,CLIP_COLLECTION} & reports[p].keys())
xworm=reports[ROOT/'testdata/hostile/xworm-v3-obfuscated-client.exe']
assert sum(t['crit']==5 for t in xworm.values())==9
assert sum(t['crit']==5 for t in reports[ROOT/'testdata/hostile/ps-cradle-stager.ps1'].values())>=1
rat_control=reports[ROOT/'testdata/triage/registry-second-review-607680-0906-8175/controls/keylog-unrelated-reply.exe']
assert sum(t['crit']==5 for t in rat_control.values())==6
for p in paths:
 if p.parent.name=='powershell-char-array-join':
  expect=p.name in ['hex-eval.ps1','decimal-eval.ps1','bom-and-payload.ps1']
  assert (OBF in reports[p])==expect
  if expect:assert reports[p][OBF]['crit']==4
summary=[{'case':p.name,'hostile':sum(t['crit']==5 for t in reports[p].values()),
 'suspicious':sum(t['crit']==4 for t in reports[p].values()),
 'module_load':MODULE in reports[p],'clipboard_read':CLIP in reports[p]} for p in paths]
(OUT/'regression-results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
