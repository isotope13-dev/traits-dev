from pathlib import Path
import json,struct,zlib,subprocess,hashlib
out=Path('/tmp/qa2-deep-review/native');out.mkdir(exist_ok=True);results=[]
for p in sorted(Path('/tmp/qa2/hostile').glob('*/*')):
 if not p.parent.name.startswith(('201707','311006')):continue
 b=bytearray(p.read_bytes());sha=hashlib.sha256(b).hexdigest();d=out/sha[:12];d.mkdir(exist_ok=True)
 run=subprocess.run(['upx','-d','-o',str(d/'standard.exe'),str(p)],capture_output=True,text=True);(d/'standard-upx.log').write_text(run.stdout+run.stderr);assert run.returncode!=0
 at=b[:4096].index(b'UPX!');ulen,clen=struct.unpack_from('<II',b,at+16);src=b[at+32:at+32+clen];pos=0;bits=0;raw=bytearray();last=1
 assert ulen<=64*1024*1024
 def byte():
  global pos
  v=src[pos];pos+=1;return v
 def bit():
  global bits,pos
  carry=bits>>31;bits=(bits<<1)&0xffffffff
  if bits:return carry
  word=struct.unpack_from('<I',src,pos)[0];pos+=4;bits=((word<<1)|1)&0xffffffff;return word>>31
 while len(raw)<=ulen:
  while bit():raw.append(byte())
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
  assert 0<dist<=len(raw) and len(raw)+length<=ulen
  for _ in range(length):raw.append(raw[-dist])
 assert len(raw)==ulen
 old=struct.unpack_from('<II',b,at+8);actual=(zlib.adler32(raw),zlib.adler32(src));struct.pack_into('<II',b,at+8,*actual);b[at+31]=sum(b[at+4:at+31])%251
 repaired=d/'analysis-copy.exe';repaired.write_bytes(b);target=d/'recovered.exe'
 if target.exists():assert target.is_file();target= d/'recovered-confirmed.exe'
 run=subprocess.run(['upx','-d','-o',str(target),str(repaired)],capture_output=True,text=True);(d/'repaired-upx.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 row={'original_sha256':sha,'original_path':str(p),'original_checksum_pair':old,'recomputed_checksum_pair':actual,'decoded_stream_size':len(raw),'recovered_path':str(target),'recovered_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'policy':'Original remains hostile because standard UPX refuses it.'};results.append(row);print(json.dumps(row))
(out/'recovery.json').write_text(json.dumps(results,indent=2)+'\n')
