from pathlib import Path
import struct,re,json
import decode_payload as d
MASK=(1<<64)-1
def rot(x,n):return ((x<<n)|(x>>(64-n)))&MASK
initial=[d.u64(0x10009ec88+16*i)^d.u64(0x10009ec90+16*i) for i in range(4)]
def h(name):
 data=name.encode();v=initial[:]
 def rnd():
  v[0]=(v[0]+v[1])&MASK;v[1]=rot(v[1],13)^v[0];v[0]=rot(v[0],32)
  v[2]=(v[2]+v[3])&MASK;v[3]=rot(v[3],16)^v[2]
  v[0]=(v[0]+v[3])&MASK;v[3]=rot(v[3],21)^v[0]
  v[2]=(v[2]+v[1])&MASK;v[1]=rot(v[1],17)^v[2];v[2]=rot(v[2],32)
 tail=(len(data)&255)<<56
 for offset in range(0,len(data)//8*8,8):
  m=int.from_bytes(data[offset:offset+8],'little');v[3]^=m;rnd();rnd();v[0]^=m
 tail|=int.from_bytes(data[len(data)//8*8:],'little');v[3]^=tail;rnd();rnd();v[0]^=tail;v[2]^=255
 for _ in range(4):rnd()
 return v[0]^v[1]^v[2]^v[3]
root=d.ROOT;targets={int(n,16) for p in (root/'decompiled').glob('*.c') for n in re.findall(r'FUN_10009b6b4\(0x([0-9a-f]+)\)',p.read_text())}
sdk=Path('/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk')
paths=[]
for base in [sdk/'usr/lib',sdk/'System/Library/Frameworks']:
 paths.extend(base.rglob('*.tbd'))
candidates=set()
# Restrict to C ABI symbols: imported Foundation/Objective-C/Swift manglings
# cannot be the short C APIs reached by these call sites.
for p in paths:
 try:content=p.read_text()
 except (OSError,UnicodeError):continue
 candidates.update(re.findall(r'\b_([A-Za-z][A-Za-z0-9_]{1,80})\b',content))
found={}
for candidate in candidates:
 for name in ['_'+candidate,candidate]:
  hashed=h(name)
  if hashed in targets:found[hex(hashed)]=name
(root/'resolved-api-hashes.json').write_text(json.dumps(found,indent=2,sort_keys=True)+'\n')
print('Resolved',len(found),'of',len(targets),'hashes using',len(candidates),'SDK API names')
print(json.dumps(found,indent=2,sort_keys=True))
