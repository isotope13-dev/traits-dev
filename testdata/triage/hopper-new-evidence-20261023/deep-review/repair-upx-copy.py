from pathlib import Path
import json,struct,zlib,subprocess
r=Path('/tmp/hopper-deep-review-20261023');row=next(x for x in json.load(open('/tmp/hopper-new-review-20261023/inventory.json')) if x['sha256'].startswith('b4fa4397c031'));original=Path(row['path']).read_bytes();b=bytearray(original);at=b.index(b'UPX!');ulen,clen=struct.unpack_from('<II',b,at+16);src=b[at+32:at+32+clen];pos=0;bits=0;out=bytearray();last=1

def byte():
 global pos
 v=src[pos];pos+=1;return v

def bit():
 global bits,pos
 carry=bits>>31;bits=(bits<<1)&0xffffffff
 if bits:return carry
 word=struct.unpack_from('<I',src,pos)[0];pos+=4;bits=((word<<1)|1)&0xffffffff;return word>>31

while len(out)<=ulen:
 while bit():out.append(byte())
 off=1
 while True:
  off=off*2+bit()
  if bit():break
 if off==2:dist=last
 else:
  encoded=(off-3)*256+byte()
  if encoded==0xffffffff:break
  dist=last=encoded+1
 length=bit()*2+bit()
 if length==0:
  length=1
  while True:
   length=length*2+bit()
   if bit():break
  length+=2
 length+=(dist>0xd00)+1
 assert 0<dist<=len(out) and len(out)+length<=ulen
 for _ in range(length):out.append(out[-dist])
assert len(out)==ulen,(len(out),ulen)
(r/'upx-raw-decoded.bin').write_bytes(out)
old=struct.unpack_from('<II',b,at+8);actual=(zlib.adler32(out),zlib.adler32(src));struct.pack_into('<II',b,at+8,*actual)
# Official UPX packhead.cpp: sum header bytes 4..30 modulo 251.
b[at+31]=sum(b[at+4:at+31])%251
print('header',b[at:at+32].hex(),'old',old,'actual',actual,'decoded',len(out))
(r/'upx-repaired-checksums.exe').write_bytes(b)

import tempfile,hashlib
with tempfile.TemporaryDirectory(prefix='upx-analysis-') as tmp:
 target=Path(tmp)/'unpacked.exe'
 rr=subprocess.run(['upx','-d','-o',str(target),str(r/'upx-repaired-checksums.exe')],capture_output=True,text=True)
 assert rr.returncode==0,rr.stderr
 result=target.read_bytes();(r/'upx-recovered-independent.exe').write_bytes(result)
 print('independently recovered SHA-256',hashlib.sha256(result).hexdigest())
