"""Inert synthetic inputs for README-member binding and Rust capability coverage."""
from pathlib import Path
import argparse,json,subprocess,os,tarfile,io
p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,default=Path('/tmp/hopper-review-boundaries'));p.add_argument('--atomscan',type=Path);args=p.parse_args();root=Path(__file__).resolve().parents[3];scratch=args.scratch;scratch.mkdir(parents=True,exist_ok=True);inputs=scratch/'inputs';inputs.mkdir(exist_ok=True);expected={}
def source(name,text,trait,want):
 (inputs/name).write_text(text);expected[name]=(trait,want)
def archive(name,members,trait,want):
 with tarfile.open(inputs/name,'w:gz') as t:
  for path,text in members.items():
   data=text.encode();info=tarfile.TarInfo(path);info.size=len(data);info.mtime=0;t.addfile(info,io.BytesIO(data))
 expected[name]=(trait,want)
readme='objectives/supply-chain/impersonation/readme-clone::readme-monorepo-subdir-title-mismatch'
manifest=json.dumps({'name':'@review/transform','version':'1.0.0','main':'index.js','repository':{'type':'git','url':'https://example.invalid/project','directory':'packages/transform'}})
def npm(heading,changelog):return {'package/package.json':manifest,'package/README.md':heading+'\n','package/CHANGELOG.md':changelog+'\n','package/index.js':'module.exports = value => value;\n'}
archive('readme-title-plus-own-changelog.tgz',npm('# Product title','# @review/transform'),readme,False)
archive('readme-title-plus-foreign-changelog.tgz',npm('# Product title','# @unrelated/identity'),readme,False)
archive('readme-foreign-identity.tgz',npm('# @foreign/native','# @review/transform'),readme,True)
archive('readme-matching-identity.tgz',npm('# @review/transform','# @review/transform'),readme,False)
archive('renamed-outer-publication.tgz',npm('# @foreign/native','# @review/transform'),readme,True)
N='metadata/package/documentation/source::markdown-h1-exact-scoped-package';R='metadata/package/documentation/package-metadata::readme-h1-exact-scoped-package'
archive('heading-observation.tgz',{'package/CHANGELOG.md':'# @review/transform\n'},N,True)
archive('readme-heading.tgz',{'package/README.md':'# @review/transform\n'},R,True)
archive('other-heading.tgz',{'package/other.md':'# @review/transform\n'},R,False)
T='objectives/privilege-escalation/token-manipulation::rust-system-process-token-impersonation'
H='micro-behaviors/crypto/decrypt::rust-app-bound-token-api-cooccurrence'
token='''fn worker() {
 let system_names = ["lsass.exe", "winlogon.exe"];
 unsafe {
  OpenProcessToken(process, rights, output);
  DuplicateToken(token, level, copy);
  ImpersonateLoggedOnUser(copy);
  RtlAdjustPrivilege(flag, enabled, thread, previous);
 }
}
'''
source('token-worker.rs',token,T,False)
source('token-renamed.rs',token.replace('worker','helper').replace('system_names','selectors').replace('process,','target,'),T,False)
source('token-qualified.rs',token.replace('DuplicateToken(', 'windows::Win32::Security::DuplicateToken('),T,False)
source('token-aliased.rs','use windows::Win32::Security::DuplicateToken as clone_token;\n'+token.replace('DuplicateToken(', 'clone_token('),T,False)
source('token-lsass-only.rs',token.replace('"winlogon.exe"','"other.exe"'),T,False)
source('token-comment.rs','/*\n'+token+'\n*/',T,False)
source('token-import-only.rs','use windows::Win32::Security::{DuplicateToken,ImpersonateLoggedOnUser};\nconst NAMES: &[&str]=&["lsass.exe","winlogon.exe"];\n',T,False)
source('token-without-system.rs',token.replace('lsass.exe','normal.exe').replace('winlogon.exe','other.exe'),T,False)
source('token-no-impersonation.rs',token.replace('ImpersonateLoggedOnUser(copy);',''),T,False)
source('token-without-open.rs',token.replace('OpenProcessToken(process, rights, output);',''),T,False)
crypto='''const PREFIX: &[u8] = b"APPB";
const VERSION: &[u8] = b"v20";
struct LocalState {app_bound_encrypted_key: String}
fn unprotect() { unsafe {
 CryptUnprotectData(input,extra,out);
 NCryptOpenKey(provider, key, name, flags);
 NCryptDecrypt(key, blob, output);
} }
'''
def crate(a=token,b=crypto):return {'library/Cargo.toml':'[package]\nname="review-library"\nversion="1.0.0"\nbuild=false\n','library/src/token.rs':a,'library/src/crypto.rs':b}
archive('source-package.tgz',crate(),H,True)
archive('source-package-renamed.tgz',{'renamed/'+k.replace('library/',''):v for k,v in crate().items()},H,True)
archive('source-no-token-calls.tgz',crate('/*\n'+token+'\n*/'),H,False)
archive('source-no-cng.tgz',crate(b=crypto.replace('NCryptDecrypt(key, blob, output);','')),H,False)
archive('source-no-dpapi.tgz',crate(b=crypto.replace('CryptUnprotectData(input,extra,out);','')),H,False)
archive('source-no-appb.tgz',crate(b=crypto.replace('b"APPB"','b"DATA"')),H,False)
archive('source-repeat-appb.tgz',crate(b=crypto.replace('b"v20"','b"APPB"')),H,False)
archive('source-api-strings.tgz',crate(a='const DOC: &str = '+json.dumps(token)+';\n'),H,False)
# Source declarations and imports do not become calls merely because they name APIs.
archive('source-token-imports.tgz',crate(a='use security::{OpenProcessToken, DuplicateToken, ImpersonateLoggedOnUser,RtlAdjustPrivilege};\nconst SYSTEM:&str="lsass.exe";\n'),H,False)
cmd=[str(args.atomscan or root/'../scan/target/release/atomscan'),'--no-update','--mode','slow','--format','json','path',str(inputs)]
r=subprocess.run(cmd,cwd=root,env=dict(os.environ,CLEAVE_TRAITS_DIR=str(root)),capture_output=True,text=True);(scratch/'boundaries.jsonl').write_text(r.stdout);(scratch/'boundaries.log').write_text(r.stderr);assert r.returncode in (0,1,2),r.stderr[-2500:]
records={}
for line in r.stdout.splitlines():
 fs=json.loads(line)['raw']['files'];records[Path(fs[0]['path']).name]={t['id']:t['crit'] for f in fs for t in f.get('traits',[])}
results=[]
for name,(trait,want) in expected.items():
 assert name in records,name
 found=trait in records[name];results.append(dict(case=name,trait=trait,expected=want,found=found,passed=want==found));print(name,'PASS' if want==found else 'FAIL')
(scratch/'boundary-results.json').write_text(json.dumps(results,indent=2)+'\n');assert all(v['passed'] for v in results),[v for v in results if not v['passed']]
print(len(results),'boundary controls passed')
