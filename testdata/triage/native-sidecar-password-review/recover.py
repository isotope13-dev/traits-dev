"""Recover constants from the pinned archive without executing sample code.

Usage: python3 recover.py ORIGINAL.tgz OUTPUT_DIRECTORY
Requires cryptography and brotli. Outputs are malicious analysis material.
"""
from pathlib import Path
import hashlib, base64, re, json, struct, gzip, tarfile, sys
import brotli
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sample=Path(sys.argv[1]);b=Path(sys.argv[2]);b.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(sample.read_bytes()).hexdigest() == '3919415f07a4da86ba6832b36ee692180cf79328178d6872c72a5cdd2825ec13'
with tarfile.open(sample) as archive:
    member=archive.getmember('package/.napi_cache');assert member.isfile()
    raw=archive.extractfile(member).read()
s=bytes(c^0x96 for c in raw).decode();(b/'sidecar-decoded.js').write_text(s)
array=re.search(r'\[([\d,]+)\]',s)
assert s[array.end():].startswith('.map(function(x){return String.fromCharCode(x)}).join(""),12))')
s=''.join(map(chr,map(int,array[1].split(','))))
s=re.sub('[a-zA-Z]',lambda m:chr((ord(m[0])-(65 if m[0].isupper() else 97)+12)%26+(65 if m[0].isupper() else 97)),s)
(b/'sidecar-loader.js').write_text(s)
for name,fn,out,encoding in [('_b','_d','bun-bootstrap.js','hex'),('_p','_dz','payload.js','b64')]:
    match=re.search(r'const '+name+r'=[^\n]*?'+fn+r'\("([a-f0-9]+)","([a-f0-9]+)","([a-f0-9]+)","([A-Za-z0-9+/=]+)"',s)
    key,iv,tag=map(bytes.fromhex,match.group(1,2,3))
    data=bytes.fromhex(match[4]) if encoding=='hex' else base64.b64decode(match[4])
    result=AESGCM(key).decrypt(iv,data+tag,None)
    if name=='_p':result=brotli.decompress(result)
    (b/out).write_bytes(result)
s=(b/'payload.js').read_text();s,end=json.JSONDecoder().raw_decode(s.split('=',1)[1]);(b/'bundle.js').write_text(s)
array=re.search(r'function _0x4bdc\(\)\{[^\[]{0,100}\[(.*?)\];',s)[1]
translation=str.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
values=[base64.b64decode(x.translate(translation)+'='*(-len(x)%4)).decode() for x in re.findall("'([^']*)'",array)]
assert len(values)==3967
rotations=[]
for rotation in range(len(values)):
    try:
        def n(i):return int(re.match(r'^[+-]?\d+',values[(i-0x1db+rotation)%len(values)])[0])
        total=-n(0xec4)*(n(0x5a2)/2)-n(0x8be)/3-n(0xf74)/4+n(0x39c)/5*(-n(0xe10)/6)-n(0xea6)/7-n(0x2e2)/8+n(0x218)/9
        if abs(total-0x443ec)<.00001:rotations.append(rotation)
    except (ValueError,TypeError):pass
assert rotations==[489]
aliases={'_0x4756'};assignments=re.findall(r'\b(_0x[\da-f]+)=(_0x[\da-f]+)\b',s)
while True:
    old=len(aliases);aliases.update(lhs for lhs,rhs in assignments if rhs in aliases)
    if old==len(aliases):break
constants={}
for match in re.finditer(r'\b(_0x[\da-f]+)=\{([^{}]*)\}',s):
    for name,value in re.findall(r'(_0x[\da-f]+):(0x[\da-f]+|\d+)',match[2]):constants[match[1]+'.'+name]=int(value,0)
def replace(match):
    if match[1] not in aliases:return match[0]
    index=constants.get(match[2]) if '.' in match[2] else int(match[2],0)
    if index is None:return match[0]
    return json.dumps(values[(index-0x1db+489)%len(values)])
s=re.sub(r'\b(_0x[\da-f]+)\((0x[\da-f]+|\d+|_0x[\da-f]+\._0x[\da-f]+)\)',replace,s)
(b/'payload-decoded.js').write_text(s)
k=hashlib.pbkdf2_hmac('sha256',b'10f9b2e09bcbc70125b77ac9cc336750ad4fd42cfcdc73a2a32ff8af1a9c2119',b'7dd5159fc78199e0fe76a3c45730726f',200000,32)
def perm(seed):
 p=list(range(256));counter=0;buf=b'';off=0
 for i in range(255,0,-1):
  lim=0xffffffff-0xffffffff%(i+1)
  while True:
   if off>=len(buf):buf=hashlib.sha256(seed+struct.pack('>Q',counter)).digest();counter+=1;off=0
   n=int.from_bytes(buf[off:off+4],'big');off+=4
   if n<=lim:break
  j=n%(i+1);p[i],p[j]=p[j],p[i]
 return p
cache={}
def dec(value):
 if value in cache:return cache[value]
 raw=base64.b64decode(value);seed=hashlib.sha256(k+raw[:16]).digest();raw=raw[16:]
 for r in range(2,-1,-1):
  out=bytearray();prev=0
  for i,c in enumerate(raw):
   p=perm(hashlib.sha256(seed+bytes([r])+str(i).encode()).digest());out.append(p.index(c)^prev);prev=c
  raw=bytes(out)
 result=raw.decode();cache[value]=result;return result
s=re.sub(r'f7bd831ae\((["\x27])([A-Za-z0-9+/=]+)\1\)',lambda m:json.dumps(dec(m[2])),s)
print('strings',len(cache),flush=True)
(b/'resources').mkdir(exist_ok=True);resources=[]
def unpack(m):
 raw=base64.b64decode(m[2]);result=gzip.decompress(AESGCM(bytes.fromhex(m[1])).decrypt(raw[:12],raw[28:]+raw[12:28],None));name=str(len(resources))+'.txt';(b/'resources'/name).write_bytes(result);resources.append({'file':name,'bytes':len(result),'prefix':result[:120].decode(errors='replace')});return json.dumps(result.decode())
s=re.sub(r'\bme\("([a-f0-9]{64})","([A-Za-z0-9+/=]+)"\)',unpack,s);(b/'payload-clear.js').write_text(s);(b/'resources.json').write_text(json.dumps(resources,indent=2));print(resources,flush=True)
