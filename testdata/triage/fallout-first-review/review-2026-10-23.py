"""Data-only controls. Never executes original or mutated specimen code.

Usage: python3 review-2026-10-23.py --samples /path/to/samples --scratch /path/to/output
Requires pefile, lief and the installed cleave. Mutations test exact evidence
relationships, while real benign fixtures and embedded hosts test near misses.
"""
import argparse,json,os,subprocess
from pathlib import Path
import pefile
ROOT=Path(__file__).resolve().parents[3]
GCM='micro-behaviors/crypto/decrypt::aes256-gcm-indirect-decrypt'
WRAP='micro-behaviors/fs/write/file/resource::rcdata-update-between-overwrite-copies-x86'
INFECT='objectives/impact/infect/resource::resource-host-wrapper-overwrite'
STAGING='objectives/command-and-control/dropper/staging/resource::resource-multi-pe-drive-scan-with-url-download'
EXFIL='objectives/exfiltration/stealer/multi-source::managed-surveillance-xor-http-request-profile'
BROAD={
 'objectives/anti-static/obfuscation/payload/loader::macho-adhoc-concealed-payload-loader',
 'objectives/anti-static/obfuscation/payload/loader::macho-adhoc-icache-flush-concealed-loader',
 'well-known/malware/stealer/foxveil::foxveil-adhoc-encoded-stealer-loader',
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--samples',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);a=ap.parse_args();a.scratch.mkdir(parents=True,exist_ok=True)
 cases=[]
 def add(path,want=(),reject=()):cases.append((path,set(want),set(reject)))
 macho=a.samples/'c7bebd02f8db/macho_c7bebd02f8db.bin'
 native=a.samples/'e7a5b0924675/2026-10-21_67ba4045844051ce28f0c906fd6f5092_amadey_elex_hijackloader_remcos_smoke-loader'
 dotnet=a.samples/'c2fdfc5fb459/cakhiatv-10-link.lol_new.exe'
 add(macho,{GCM}|BROAD);add(native,{WRAP,INFECT,STAGING});add(dotnet,{EXFIL})
 # Native matcher binds the same temporary path across two calls.
 b=native.read_bytes();pat=bytes.fromhex('6a008b45e8508d8db8f9ffff51ff1500255100');assert b.count(pat)==1
 for name,old,new in [('different-temp.exe',pat,pat.replace(bytes.fromhex('b8f9ffff'),bytes.fromhex('b0f9ffff'))),('icon-update.exe',bytes.fromhex('68000400006a636a0a8b95'),bytes.fromhex('68000400006a636a038b95'))]:
  assert b.count(old)==1;path=a.scratch/name;path.write_bytes(b.replace(old,new));add(path,reject={WRAP,INFECT,STAGING})
 # Break the verified GCM ABI without removing the rest of the loader.
 b=macho.read_bytes();pat=bytes.fromhex('c745c40000000048c745c82000000048c745d00c00000048c745b010000000');assert b.count(pat)==1
 for name,at,value in [('key24.macho',11,24),('tag12.macho',27,12)]:
  replacement=bytearray(pat);replacement[at]=value;path=a.scratch/name;path.write_bytes(b.replace(pat,replacement));add(path,reject={GCM})
 # Retain signing, blob, dispatch and cache facts but erase the matched timer.
 original=macho.read_bytes();changed=bytearray(original);changed[1375044:1375094]=bytes(50)
 path=a.scratch/'no-timing-evidence.macho';path.write_bytes(changed);add(path,{GCM},BROAD)
 # The original host and bundled helper programs are not infectors.
 pe=pefile.PE(data=native.read_bytes())
 for typ in pe.DIRECTORY_ENTRY_RESOURCE.entries:
  for name in typ.directory.entries:
   for lang in name.directory.entries:
    r=lang.data.struct;content=pe.get_data(r.OffsetToData,r.Size)
    if content.startswith(b'MZ'):
     path=a.scratch/('resource-'+str(name.name or name.id)+'.exe');path.write_bytes(content);add(path,reject={WRAP,INFECT,EXFIL})
 for name in ['managed-status-stubs-only.exe','managed-native-interop-only.exe','ffplay-media-controls/ffplay.exe','v8-runtime-entitlement-controls.macho.xz','pyext-entry-stub.macho']:
  add(ROOT/'testdata/benign'/name,reject=BROAD|{INFECT,EXFIL})
 results=[]
 for path,want,reject in cases:
  run=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--disable','third-party','--format','json',str(path)],capture_output=True,text=True,check=True)
  report=json.loads(run.stdout);outer=report['files'][0];ids={t['id'] for t in outer.get('traits',[])}
  assert want<=ids,(str(path),'missing',want-ids)
  assert not reject&ids,(str(path),'unexpected',reject&ids)
  results.append({'path':str(path),'required':sorted(want),'forbidden':sorted(reject),'passed':True});print('PASS',path.name,flush=True)
 (a.scratch/'results.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
