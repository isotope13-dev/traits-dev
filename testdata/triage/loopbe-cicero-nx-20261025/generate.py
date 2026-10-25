"""Small, inert structural controls; no keys, endpoints or specimen identity."""
from pathlib import Path
import io,json,struct,tarfile
out=Path(__file__).parent

def pe(increment, feedback=True, inline=True, executable=True):
 b=bytearray(0x8400); b[:2]=b'MZ';struct.pack_into('<I',b,0x3c,0x80);b[0x80:0x84]=b'PE\0\0'
 struct.pack_into('<HHIIIHH',b,0x84,0x14c,2,0,0,0,0xe0,0x102)
 o=0x98;struct.pack_into('<H',b,o,0x10b)
 for off,v in [(16,0x1000),(20,0x1000),(24,0x2000),(28,0x400000),(32,0x1000),(36,0x200),(56,0x9000),(60,0x400),(92,16)]:struct.pack_into('<I',b,o+off,v)
 struct.pack_into('<H',b,o+68,2)
 for i,(name,rva,raw,size,flags) in enumerate([(b'.text',0x1000,0x400,0x1000,0xe0000020),(b'.rsrc',0x2000,0x1400,0x7000,0xe0000020 if executable else 0xc0000040)]):
  h=0x178+40*i;b[h:h+len(name)]=name;struct.pack_into('<IIII',b,h+8,size,rva,size,raw);struct.pack_into('<I',b,h+36,flags)
 x=bytearray.fromhex('5e89f7b93b00000085c9740780365f4649ebf557c3e8e6ffffff')
 if not inline:x[20]=0x90
 b[0x400:0x400+len(x)]=x
 x=bytearray.fromhex('09c9741d0fafc2'+increment+'89c3c1e303c1e81d09d888c3301e0fb61e01d84649ebdfffe5')
 if not feedback:x[x.index(bytes.fromhex('01d8'))]=0x90
 b[0x1400:0x1400+len(x)]=x
 return b
for n,args in {'sub':('83e8ed',),'add':('83c013',),'lea':('8d4013',),'missing-feedback':('83e8ed',False),'missing-inline':('83e8ed',True,False),'nonexecutable-resource':('83e8ed',True,True,False)}.items():(out/(n+'.exe')).write_bytes(pe(*args))
# Preserve every existing clone predicate. Vary only the claimed package or
# repository, so the exclusion cannot silence a rename outside the Nx scope.
with tarfile.open(out.parent/'commonly-version-drift/foreign-link.tgz') as t:
 source={m.name:t.extractfile(m).read() for m in t if m.isfile()}
for n,name,repo in [('official','@nx/js','https://github.com/nrwl/nx.git'),('renamed','@example/js','https://github.com/nrwl/nx.git'),('foreign-repository','@nx/js','https://github.com/example/other.git')]:
 files=dict(source);manifest=json.loads(files['package/package.json']);manifest.update(name=name,repository={'type':'git','url':repo,'directory':'packages/js'});files['package/package.json']=json.dumps(manifest).encode()
 registry=json.loads(files['release.registry.json']);registry['name']=name;files['release.registry.json']=json.dumps(registry).encode()
 with tarfile.open(out/('nx-'+n+'.tgz'),'w:gz') as t:
  for path,data in files.items():
   info=tarfile.TarInfo(path);info.size=len(data);info.mtime=0;t.addfile(info,io.BytesIO(data))
