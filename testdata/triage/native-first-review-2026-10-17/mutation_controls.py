"""Mutation controls for the reviewed native signatures; never executes samples."""
import argparse,hashlib,json,subprocess,concurrent.futures
from pathlib import Path
import pefile
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--samples',nargs=3,required=True,help='myRunner, WannaCry, Beacon bundle')
parser.add_argument('--work-dir',type=Path,required=True)
args=parser.parse_args()
OUT=args.work_dir
OUT.mkdir(parents=True,exist_ok=True)
SAMPLES=args.samples
EXPECTED_SHA256=[
 '3604f399140d0e9c0b4883cfc35c4ba903bbaeee1578db52acac1d0347d32a9a',
 '6d1ad09f5f069090fb3dd76c8182688ef83e0dfa5853b3d62af8c73daf72991b',
 'a9e4200b9fa36261c6f82803419035963afb95f04617a766ba504c85ab2e8fb7',
]
for sample,expected in zip(SAMPLES,EXPECTED_SHA256):
 assert hashlib.sha256(Path(sample).read_bytes()).hexdigest()==expected,sample
# Extract only the two PE members addressed by these pinned regression cases.
for index,offset,name in [(1,0x320a4,'1-embedded-320a4.exe'),(2,0x4bc201,'2-embedded-4bc201.exe')]:
 data=Path(SAMPLES[index]).read_bytes()[offset:]
 pe=pefile.PE(data=data,fast_load=True)
 end=max(section.PointerToRawData+section.SizeOfRawData for section in pe.sections)
 (OUT/name).write_bytes(data[:end])

CASES=[]
def mutated(name,source,edits,rules,expect):
 b=bytearray(Path(source).read_bytes())
 for offset,before,after in edits:
  assert b[offset:offset+len(before)]==before,(name,hex(offset))
  assert len(before)==len(after)
  b[offset:offset+len(before)]=after
 p=OUT/name;p.write_bytes(b);CASES.append((str(p),rules,expect))
wc='well-known/malware/ransomware/wannacry::'
cs='well-known/malware/rat/cobalt-strike/config::'
mutated('wc-restored-conditional.exe',SAMPLES[1],[(0x81a5,b'\x90\x90',b'\x75\x07')],[wc+'wannacry-disabled-url-killswitch'],[False])
payload=OUT/'1-embedded-320a4.exe';p=pefile.PE(str(payload),fast_load=True)
off=p.get_offset_from_rva(0x1564);b=payload.read_bytes()
mutated('wc-no-header-check.exe',payload,[(off,b[off:off+30],b'\x90'*30)],[wc+'wannacry-encrypted-resource-payload'],[False])
off=b.find(b'WNcry@2ol7')
mutated('wc-no-password.exe',payload,[(off,b'WNcry@2ol7',b'0123456789')],[wc+'wannacry-encrypted-resource-payload'],[False])
beacon=OUT/'2-embedded-4bc201.exe';b=beacon.read_bytes();off=0x2f228
mutated('beacon-prefix-only.dll',beacon,[(off+19,b[off+19:off+20],bytes([b[off+19]^1]))],[cs+'xor-encoded-config-reflective-beacon',cs+'xor-0x69-config-block'],[False,False])
enc=b[off:off+4096]
mutated('beacon-xor2e.dll',beacon,[(off,enc,bytes(x^0x69^0x2e for x in enc))],[cs+'xor-encoded-config-reflective-beacon',cs+'xor-0x2e-config-block'],[True,True])
mutated('beacon-variable-timing.dll',beacon,[(off+22,b[off+22:off+26],bytes(x^0x69 for x in b'\x00\x00\xea\x60'))],[cs+'xor-encoded-config-reflective-beacon'],[True])
b=Path(SAMPLES[0]).read_bytes();pattern=bytes.fromhex('6a2e52ffd583c408c60000')
offsets=[];pos=0
while True:
 pos=b.find(pattern,pos)
 if pos<0:break
 offsets.append(pos);pos+=1
mutated('myrunner-no-extension-truncation.exe',SAMPLES[0],[(o,pattern,b'\x90'*len(pattern)) for o in offsets],['objectives/evasion/hijack-execution-flow/file-association::extensionless-executable-association-wrapper','objectives/execution/payload/file-exec::pop3-tagged-exe-association-loader'],[False,False])
CASES.append((SAMPLES[0],['metadata/file/encoding::pe-code-base64-shaped-string','micro-behaviors/fs/path/application/executable::mshta-name-reference'],[False,False]))
def run(case):
 path,rules,expect=case
 r=subprocess.run(['cleave','test-rules',path,'--rules',','.join(rules)],capture_output=True,text=True)
 text=r.stdout+r.stderr
 actual=[any(line.startswith('MATCHED '+rule+' ') for line in text.splitlines()) for rule in rules]
 assert actual==expect,(path,actual,expect,text)
 assert 'validation failed' not in text,text
 (OUT/(Path(path).name+'.control.txt')).write_text(text)
 return dict(file=Path(path).name,rules=rules,expected=expect,actual=actual)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(run,CASES))
(OUT/'control-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))

