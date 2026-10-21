import pathlib,json,subprocess,os,concurrent.futures,sys,tempfile
if len(sys.argv)!=2:
 raise SystemExit('usage: run-controls.py /path/to/Invoke-SMBExec.ps1')
b=pathlib.Path(tempfile.mkdtemp(prefix='ntlm-hash-controls-'))
s=pathlib.Path(sys.argv[1]).read_text()
out=b/'controls';out.mkdir()
rule='objectives/lateral-movement/pass-the-hash/ntlm::powershell-raw-hash-service-execution'
create='micro-behaviors/os/service/create::scm-create-service-packet'
delete='micro-behaviors/os/service/delete::scm-delete-service-packet'
variants={
 'renamed-file':(s,[rule,create,delete],[]),
 'password-derived':(s.replace('[String]$Hash,','[String]$Password,').replace('$NTLM_hash_bytes = (&{for ($i = 0;$i -lt $hash.Length;$i += 2){$hash.SubString($i,2)}}) -join "-"','$NTLM_hash_bytes = Get-NTHash $Password'),[create,delete],[rule]),
 'raw-hash-client':('\n'.join(l for l in s.splitlines() if '= Get-PacketSCMCreateServiceW' not in l and '= Get-PacketSCMDeleteServiceW' not in l),[],[rule,create,delete]),
 'mac-key-unrelated':(s.replace('$HMAC_MD5.key = $NTLM_hash_bytes','$HMAC_MD5.key = $SessionKey'),[create,delete],[rule]),
 'builder-declarations':('function Get-PacketSCMCreateServiceW { param($Command) }\nfunction Get-PacketSCMDeleteServiceW { param($Handle) }',[],[create,delete,rule]),
}
def run(item):
 name,(src,yes,no)=item;p=out/(name+'.ps1');p.write_text(src)
 f=out/(name+'.json');e=out/(name+'.err')
 with f.open('w') as fo,e.open('w') as fe:r=subprocess.run(['cleave','--format','json',str(p)],stdout=fo,stderr=fe,env={**os.environ,'CLEAVE_VALIDATE':'0'},timeout=120)
 assert r.returncode==0,(name,r.returncode,e.read_text()[-2000:])
 obj=json.loads(f.read_text());raw=obj.get('raw',obj);files=raw.get('files',[])
 ids={t['id'] for q in files for t in q.get('traits',q.get('findings',[]))}
 assert all(x in ids for x in yes),(name,'missing',set(yes)-ids)
 assert not(set(no)&ids),(name,'unexpected',set(no)&ids)
 return {'control':name,'required':yes,'absent':no,'passed':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:results=list(p.map(run,variants.items()))
(b/'control-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));print('Results:',b)
