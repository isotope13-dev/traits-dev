"""Offline recovery for c7bebd02f8db; validates every GCM tag and both hashes.
Requires lief and cryptography. Addresses refer to the inspected x86_64 slice.
"""
import argparse,lief,struct,hashlib,hmac,json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pathlib import Path
ap=argparse.ArgumentParser(description='Data-only recovery; never runs specimen code')
ap.add_argument('--sample',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
a=ap.parse_args();p=a.output;p.mkdir(parents=True,exist_ok=True)
m=lief.MachO.parse(str(a.sample)).at(0)
def rd(a,n):return bytes(m.get_content_from_virtual_address(a,n))
def u32(a):return struct.unpack('<I',rd(a,4))[0]
def u64(a):return struct.unpack('<Q',rd(a,8))[0]
def xor(a,b):return bytes(x^y for x,y in zip(a,b))
def hkdf(ikm,salt,info,n):
 prk=hmac.digest(salt or bytes(32),ikm,'sha256');return hmac.digest(prk,info+b'\x01','sha256')[:n]
def decode(a,n):
 vals=[];tab=rd(0x100072810,256)
 for c in rd(a, n*3+100):
  v=((0x81*c+0xad)&255)^tab[c]
  if v!=0xa8:vals.append(v)
  if len(vals)*3//4>=n and len(vals)%4==0:break
 out=bytearray()
 for i in range(0,len(vals),4):
  a,b,c,d=vals[i:i+4]; v=(a<<18)|(b<<12)|(c<<6)|d;out+=v.to_bytes(3,'big')
 return bytes(out[:n])
seed=u64(0x100074020)^u64(0x100074028)
salt=xor(rd(0x100074130,32),rd(0x100074150,32))
info=xor(rd(0x100074184,13),rd(0x100074191,13))+b'\0\0\0'
print('seed',hex(seed),'salt',salt.hex(),'info',info)
base=0x10007242c;tags=0x100072514;sizes=0x100072600;types=rd(0x1000723f0,58)
ct=[]
for i in range(58):
 a=base+4*i; a=base+struct.unpack('<i',rd(a,4))[0]; t=tags+4*i;t=tags+struct.unpack('<i',rd(t,4))[0]
 ct.append((decode(a,u64(sizes+8*i)),rd(t,16)))
textsec=next(s for s in m.sections if s.name=='__text')
th=hashlib.sha256(bytes(textsec.content)).digest()
print('text hash',th.hex())
for mask in [0,0x342464b0]:
 password=struct.pack('>I',(u32(0x10007404e)^seed^mask^struct.unpack('<I',th[:4])[0])&0xffffffff)+xor(rd(0x10007404e,32),th)
 key=hashlib.pbkdf2_hmac('sha256',password,salt,0x13982,32)
 try:
  outputs=[]
  for i,(cipher,tag) in enumerate(ct):
   nonce=hkdf(key,None,info+bytes([i]),12)
   out=AESGCM(key).decrypt(nonce,cipher+tag,None)
   if types[i]==0xe1:outputs.append(out)
  out=b''.join(outputs);(p/'macho-payload.applescript').write_bytes(out)
  assert hashlib.sha256(out).digest()==xor(rd(0x100074af0,32),rd(0x100074b10,32))
  (p/'macho-recovery.json').write_text(json.dumps({'payload_sha256':hashlib.sha256(out).hexdigest(),'payload_bytes':len(out),'authenticated_chunks':58,'retained_chunks':sum(t==0xe1 for t in types),'text_sha256':th.hex(),'iterations':0x13982,'key':key.hex()},indent=2)+'\n')
  print('SUCCESS',mask,len(out),hashlib.sha256(out).hexdigest());break
 except Exception as e: print('failed',hex(mask),type(e).__name__)
else:raise ValueError('No key candidate authenticated every chunk')

key=hkdf(struct.pack('<Q',seed),xor(rd(0x1000740f0,32),rd(0x100074110,32)),rd(0x100072390,18),32)
info=xor(rd(0x100074170,10),rd(0x10007417a,10))+b'\0\0\0'
outputs=[]
for i in range(4):
 base=0x1000723a8;tags=0x1000723b8
 a=base+struct.unpack('<i',rd(base+4*i,4))[0];t=tags+struct.unpack('<i',rd(tags+4*i,4))[0]
 out=AESGCM(key).decrypt(hkdf(key,None,info+bytes([i]),12),decode(a,u64(0x1000723d0+8*i))+rd(t,16),None)
 if rd(0x1000723a2+i,1)==b'\xe1':outputs.append(out)
out=b''.join(outputs);assert len(out)==402
assert hashlib.sha256(out).digest()==xor(rd(0x100074ab0,32),rd(0x100074ad0,32))
(p/'macho-bootstrap.scpt').write_bytes(out);print('BOOTSTRAP',hashlib.sha256(out).hexdigest())
