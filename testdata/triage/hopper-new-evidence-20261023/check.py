#!/usr/bin/env python3
"""Static detector boundary checks; never runs a sample or contacts sample URLs."""
import argparse,base64,hashlib,json,os,pathlib,re,subprocess
p=argparse.ArgumentParser();p.add_argument('--samples',default='/var/tmp/hopper-triage/new');p.add_argument('--work',default='/tmp/hopper-new-boundaries-20261023');p.add_argument('--cleave',default='../cleave/target/release/cleave');a=p.parse_args();root=pathlib.Path.cwd();work=pathlib.Path(a.work);work.mkdir(parents=True,exist_ok=True)
base=pathlib.Path(a.samples);relocated=pathlib.Path('/tmp/triage/misplaced-good/hopper-new-evidence-20261023')
def sample(rel):
 f=base/rel
 return f if f.exists() else relocated/rel
cases=[]
def add(name,data,required=(),forbidden=(),max_high=None):
 path=work/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data.encode() if isinstance(data,str) else data);cases.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'required':list(required),'forbidden':list(forbidden),'max_high':max_high})
outer=sample('bazaar/script..js').read_text();html=base64.b64decode(re.search(r'atob\("([A-Za-z0-9+/=]+)"',outer).group(1)).decode()
exfil='objectives/exfiltration/messaging/telegram::browser-password-report-telegram-post';lure='objectives/credential-access/phishing/lure::email-password-telegram-false-retry';encoded='objectives/anti-static/obfuscation/eval/browser::base64-document-writer-conceals-password-harvest'
add('encoded-page.js',outer,required=[exfil,lure,encoded]);add('decoded-page.html',html,required=[exfil,lure],forbidden=[encoded])
renamed=re.sub(r'\b(passwordInput|messageText|telegramApiUrl|telegramRes|TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID)\b',lambda m:'renamed_'+m.group(1),html)
add('renamed-variables.html',renamed,required=[exfil,lure])
for name,text in [('no-bot-endpoint',html.replace('api.telegram.org/bot','example.invalid/bot')),('no-password-report',html.replace("Password: ' + password","Status: ' + password")),('no-password-input',html.replace('type="password"','type="text"')),('no-post',html.replace("method: 'POST'","method: 'GET'")),('no-chat-body',html.replace('chat_id: TELEGRAM_CHAT_ID','destination: TELEGRAM_CHAT_ID'))]:add(name+'.html',text,forbidden=[exfil,lure,encoded])
add('no-email-pretext.html',html.replace('Enter your current email password','Enter your account code').replace('enter your current email password','enter your account code'),required=[exfil],forbidden=[lure])
add('ordinary-bot-notify.html','<script>fetch("https://api.telegram.org/botTOKEN/sendMessage", {method:"POST",body:JSON.stringify({chat_id:12,text:"build completed"})});</script>',forbidden=[exfil,lure,encoded])
add('ordinary-password-form.html','<form><input type="email"><input type="password"><button>Login</button></form>',forbidden=[exfil,lure,encoded])
add('process-monitor-label.exe',sample('triage/2026-10-22_d8841b43d36eaea0eaaef759fdc778f4_cobalt-strike_glassworm_icedid_njrat_remcos_satacom').read_bytes(),required=['micro-behaviors/ui/menu::process-monitor-label'],forbidden=['objectives/anti-analysis/sandbox-detect/tool-references::process-monitor'],max_high=0)
add('go-gzip-control.go',sample('upload/go-gzip-stage-exec.go').read_bytes(),required=['micro-behaviors/process/create/local-exec::go-command-temporary-path'],forbidden=['objectives/command-and-control/backdoor/tasking/filesystem::go-decoded-file-task-execute'])
# A concrete Microsoft service-host version claim plus randomized Go code.
rel='triage/2026-10-22_d17c86442f59c61ea76f92aaca0cd3f5_coinminer_dosia_glassworm_poet-rat_quasar-rat_snatch';blob=sample(rel).read_bytes();impersonation='objectives/evasion/masquerade/version-resource/service-host::garbled-go-microsoft-service-host-impersonation'
add('renamed-service-host.exe',blob,required=[impersonation]);old='Microsoft Corporation'.encode('utf-16le');new='Private Laboratory   '.encode('utf-16le');assert len(old)==len(new) and old in blob
add('non-microsoft-company.exe',blob.replace(old,new),forbidden=[impersonation]);old='svchost.exe'.encode('utf-16le');new='program.exe'.encode('utf-16le');assert len(old)==len(new) and old in blob
add('non-service-name.exe',blob.replace(old,new),forbidden=[impersonation])
# UPX integrity failure is suspicious metadata, not a hostile behavioral claim.
rel='triage/2026-10-22_d30f15580a416e111d16d67877b45a87_coinminer_elex_rhadamanthys_stop';add('checksum-failure.exe',sample(rel).read_bytes(),required=['metadata/binary/layout/compression::upx-checksum-mismatch'],forbidden=['objectives/anti-static/obfuscation/pack::upx-checksum-mismatch'])
# A Steam URL by itself is ordinary service content. Build a small control,
# but do not execute it.
c=work/'profile.c';c.write_text('const char profile[]="https://steamcommunity.com/profiles/123456789"; int main(void){return profile[0]==0;}\n');exe=work/'profile-control';subprocess.run(['cc','-O0',str(c),'-o',str(exe)],check=True,capture_output=True);add('steam-profile-control',exe.read_bytes(),required=['micro-behaviors/communications/http/services/steam::steam-profile-url'],forbidden=['objectives/command-and-control/channel/deaddrop/steam::steam-deaddrop'],max_high=0)
env=os.environ.copy();env['XDG_CACHE_HOME']=str(work/'cache');cmd=[str(pathlib.Path(a.cleave).resolve()),'--no-update-check','--traits-dir',str(root),'analyze','--format','json']+[x['path'] for x in cases];r=subprocess.run(cmd,env=env,text=True,capture_output=True);(work/'stderr.log').write_text(r.stderr);assert r.returncode==0,r.stderr
reports=[];s=r.stdout.lstrip();decoder=json.JSONDecoder()
while s:
 d,n=decoder.raw_decode(s);reports.append(d);s=s[n:].lstrip()
by={f['path']:f for d in reports for f in d['files']};failed=[]
for c in cases:
 f=by[c['path']];ts={t['id']:t for t in f.get('traits',[])};high=[t for t in ts.values() if t.get('crit',0)>=4];c['high_findings']=[{k:t[k] for k in ['id','crit','desc']} for t in high];c['failures']=[f'missing {i}' for i in c['required'] if i not in ts]+[f'unexpected {i}' for i in c['forbidden'] if i in ts]
 if c['max_high'] is not None and len(high)>c['max_high']:c['failures'].append(f'{len(high)} high findings exceeds {c["max_high"]}')
 if c['failures']:failed.append(c)
out={'command':cmd,'passed':len(cases)-len(failed),'failed':len(failed),'cases':cases};(work/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'failed':out['failed'],'failures':failed},indent=2));raise SystemExit(bool(failed))
