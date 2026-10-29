from pathlib import Path
import struct,hashlib,re,subprocess,json
r=Path(__import__("sys").argv[1])
results=[]
for h,fun in [('82b03053f38e','655c71a0'),('74e1d8874281','655c1ae0')]:
 d=r/'extracted'/h;pyd=(d/'pyarmor_runtime_000000_pyarmor_runtime.pyd').read_bytes();pe=struct.unpack_from('<I',pyd,60)[0];ns,opts=struct.unpack_from('<H',pyd,pe+6)[0],struct.unpack_from('<H',pyd,pe+20)[0];base=struct.unpack_from('<Q',pyd,pe+24+24)[0];sections=[struct.unpack_from('<IIII',pyd,pe+24+opts+i*40+8) for i in range(ns)]
 def read(va,n):
  rv=va-base
  for vs,vaddr,sz,off in sections:
   if vaddr<=rv<vaddr+sz:return pyd[off+rv-vaddr:off+rv-vaddr+n]
  raise ValueError(hex(va))
 ident=pyd.index(b'pyarmor-vax-000000');meta=ident+0x24;puboff,publen,licoff=struct.unpack_from('<III',pyd,meta);start=ident+0x34;lic=start+licoff;liclen=struct.unpack_from('<I',pyd,lic+4)[0]
 c=(r/'ghidra'/f'{h}-pyarmor'/f'{fun}.c').read_text();saltva=int(re.findall(r'puVar\w+ = &DAT_([0-9a-f]+);',c)[0],16);salt=bytes(v^0xf1 for v in read(saltva,0x10e));key=hashlib.md5(pyd[ident:ident+20]+pyd[start+puboff:start+puboff+publen]+pyd[lic+0x20:lic+0x20+liclen]+salt).digest()
 for f in d.glob('*.pyc'):
  b=f.read_bytes();pos=b.find(b'PY000000')
  if pos<0:continue
  blob=bytearray(b[pos:]);off,n,flags=struct.unpack_from('<III',blob,0x1c);iv=struct.pack('<I',flags)+blob[0x2c:0x34];cipher=blob[off:off+n]
  q=subprocess.run(['openssl','enc','-aes-128-ctr','-K',key.hex(),'-iv',(iv+b'\0\0\0\2').hex(),'-nopad'],input=cipher,stdout=subprocess.PIPE,stderr=subprocess.PIPE);plain=q.stdout;(d/(f.stem+'.decrypted.bin')).write_bytes(plain)
  v={'sample':h,'file':f.name,'key':key.hex(),'iv':iv.hex(),'offset':off,'length':n,'flags':hex(flags),'plain_header':plain[:32].hex(),'header_matches':len(plain)>=16 and struct.unpack_from('<I',plain,12)[0]==flags};print(v);results.append(v)
(r/'rizin/pyarmor-decryption.json').write_text(json.dumps(results,indent=2)+'\n')
