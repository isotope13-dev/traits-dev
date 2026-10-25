"""Focused regressions. CLEAVE selects the analyzer; no sample code executes."""
import concurrent.futures,json,os,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[3]
fixtures=pathlib.Path(__file__).resolve().parent
scratch=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-9f-e1-eb')
C='objectives/impact/ui/manipulation/social::remote-config-social-follow-like-automation'
E='objectives/exfiltration/stealer/credential::social-login-password-response-exfiltration'
X='micro-behaviors/data/arithmetic::indexed-xor-array-assignment'
J='micro-behaviors/data/format/credentials::jwt-pattern-prefix'
G='micro-behaviors/process/debug/tool-markers::gdb-name-reference'
W='micro-behaviors/fs/write/file/redirect::shell-cat-heredoc-file-write'
A='micro-behaviors/crypto/encrypt::forge-aes-gcm-encryptor'
R='micro-behaviors/crypto/encrypt::rsa-pkcs1-v1-5-encrypt-call'
B='micro-behaviors/data/decode/base64::base64-decode-call-text'
N='micro-behaviors/data/encode/base64::forge-encode64-call'
H=['objectives/anti-static/obfuscation/payload/resource::base85-xor-resource-image-concealment','objectives/execution/payload/image-map::concealed-resource-thread-image-activation','objectives/evasion/masquerade/identity/mimicry::unsigned-update-assistant-concealed-image']
cases=[
 (fixtures/'regex-reference.py',[J,G],[]),
 (fixtures/'xor-assignment.js',[X],[]),
 (fixtures/'encoded-near-miss.txt',[],[J,G,X]),
 (fixtures/'crypto.js',[A,R,B,N],[C,E]),
 (fixtures/'crypto-references.js',[],[A,R,B,N]),
 (fixtures/'heredoc.sh',[W],[]),
 (fixtures/'heredoc-quoted.sh',[],[W]),
 (fixtures/'manual-engagement.js',[],[C,E]),
 (fixtures/'ordinary-login.js',[],[C,E]),
 (fixtures/'login-activation.js',[C],[E]),
 (fixtures/'login-leak.js',[E],[C]),
 (root/'testdata/triage/stranded-xmrig-members/xor-assignment.js',[X],[]),
 (root/'testdata/triage/stranded-xmrig-members/xor-comparison.js',[],[X]),
 (root/'testdata/hostile/jwt-clipboard-capture-controls.js',[J],[]),
 (root/'testdata/benign/secret-redaction-table-controls.py',[J],[]),
 (root/'testdata/taxonomy/python-security-triage/analysis-gate.py',[G],[]),
 (root/'testdata/benign/pxt-first-review/gdb-endpoint.js',[],[G]),
 (scratch/'without-entry-call.exe',[],H),
 (scratch/'renamed-resources.exe',H,[G,J,X]),
 (scratch/'encoded-resource.txt',[],[G,J,X]),
]
def check(case):
 p,present,absent=case
 if not p.exists():return {'path':str(p),'skip':'optional original-derived scratch control absent'}
 cp=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(root),'--format','json',str(p)],capture_output=True,text=True,env={**os.environ,'CLEAVE_FORMAT':'json'},cwd=root)
 if cp.returncode:raise AssertionError((str(p),cp.stderr[-2500:]))
 report=json.loads(cp.stdout);ts={t['id'] for f in report['files'] for t in f.get('traits',[])}
 assert not (set(present)-ts),(str(p),'missing',set(present)-ts)
 assert not (set(absent)&ts),(str(p),'unexpected',set(absent)&ts)
 return {'path':str(p),'required':present,'forbidden':absent,'passed':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(check,cases))
(scratch/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
print('Passed',sum(x.get('passed',False) for x in results),'focused controls')
