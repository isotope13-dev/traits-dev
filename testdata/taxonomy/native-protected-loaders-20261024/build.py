"""Build inert code/data controls. All entry points immediately return.
The byte snippets describe reusable protector routines, never a malware payload.
"""
import struct, random
from pathlib import Path
ROOT=Path(__file__).parent
DECODER=bytes.fromhex('83ec24568b44242c0fb6080fb6500180f1a380f254884c24040fb64802885424050fb65003f6d180f275884c24060fb64804885424070fb6500580f1e780f244884c24080fb64806885424090fb6500780f14b80f223884c240a0fb648088854240b0fb6500980f1bf80f245884c240c0fb6480a8854240d0fb6500b80f13b80f256884c240e0fb6480c8854240f0fb6500d80f1f880f298884c24100fb6480e885424110fb6500f80f15b80f2f4884c24120fb64810885424130fb6501180f1b580f287884c24140fb64812885424150fb6501380f17b80f20f884c24160fb64814885424170fb6501580f1f480f276884c24180fb64816885424190fb6501780f1b980f234884c241a0fb648188854241b0fb6501980f1bf80f21e884c241c0fb6481a8854241d0fb6501b8b74243080f1e780f278884c241e0fb6481c8854241f0fb6501d80f19880f2e9884c24200fb6481e885424210fb6501f6a208d4424085080f16f80f2b456884c242e8854242fc644243000e8849b000083c40c8bc65e83c424c3')
GATE=bytes.fromhex('c6442418e0c64424193bc644241a8dc644241b2ac644241ca2c644241d2ac644241e2ac644241f41c6442420d3c644242120c644242264c644242306c64424248ac6442425f7c64424263dc64424279dc6442428d9c6442429eec644242a15c644242b68c644242cf4c644242d76c644242eb9c644242f34c6442430bfc64424311ec6442432e7c644243378c644243498c6442435e9c64424366fc6442437b4885c2438e897fbffff50e8df9e000083c40c3da0b241000f84bd090000ff')
APLIB=bytes.fromhex('fcb2808a0648ffc6880748ffc7bb0200000000d275078a1648ffc610d273e400d275078a1648ffc6')
LOAD=bytes.fromhex('555750e80000000083c40c56ff15000000009090909090909090909090908b388d4c24208be881c7b4000000e8000000008b0f505655ffd1')
def pe(sections,bits=32,entry=0x1000,extra_size=0):
    b=bytearray(512);b[:2]=b'MZ';struct.pack_into('<I',b,60,128);b[128:132]=b'PE\0\0'
    opt=0x98;optsize=224 if bits==32 else 240
    struct.pack_into('<HHIIIHH',b,132,0x14c if bits==32 else 0x8664,len(sections),1700000000,0,0,optsize,0x102 if bits==32 else 0x22)
    struct.pack_into('<H',b,opt,0x10b if bits==32 else 0x20b)
    struct.pack_into('<I',b,opt+16,entry)
    if bits==32:struct.pack_into('<I',b,opt+28,0x400000)
    else:struct.pack_into('<Q',b,opt+24,0x140000000)
    for o,v in [(32,4096),(36,512),(60,512),(92 if bits==32 else 108,16)]:struct.pack_into('<I',b,opt+o,v)
    struct.pack_into('<H',b,opt+68,3)
    end=0
    for i,(name,rva,data,flags,vsize) in enumerate(sections):
        pos=len(b) if data else 0;size=(len(data)+511)&~511
        struct.pack_into('<8sIIIIIIHHI',b,opt+optsize+i*40,name.encode(),vsize or len(data),rva,size,pos,0,0,0,0,flags)
        if data:b.extend(data+b'\0'*(size-len(data)))
        end=max(end,rva+(vsize or len(data)))
    struct.pack_into('<I',b,opt+56,(end+4095)&~4095)
    if extra_size>len(b):b.extend(b'\0'*(extra_size-len(b)))
    return bytes(b)
def native(kind):
    text=bytearray(b'\x90'*2048);text[0]=0xc3;text[256:256+len(DECODER)]=DECODER
    gate=bytearray(GATE);struct.pack_into('<i',gate,165,256-(1024+169))
    if kind=='wrong-call':struct.pack_into('<i',gate,165,16)
    if kind=='wrong-variable':gate[4]^=1
    if kind=='no-gate':gate=b'\x90'*len(gate)
    text[1024:1024+len(gate)]=gate
    # Native AppDomain.Load(byte[]) invocation and its COM identities.
    text[1600:1600+len(LOAD)]=LOAD
    if kind=='no-load':text[1600:1600+len(LOAD)]=b'\x90'*len(LOAD)
    ids=bytes.fromhex('dc96f605292b6336ad8bc4389cf2a7138d1880928e0e6748b30c7fa83884e8de9edb32d3b3b925418207a14884f53216')
    return pe([('.text',4096,bytes(text),0x60000020,0),('.rdata',8192,ids,0x40000040,0)])
def bootstrap(kind):
    rng=random.Random(42);b=bytearray(rng.randbytes(1048576));b[0]=0xc3;b[128:128+len(APLIB)]=APLIB
    if kind=='no-depacker':b[128:128+len(APLIB)]=b'\x90'*len(APLIB)
    memory=b'' if kind!='file-backed-code' else b'\xc3'
    return pe([('.winlice',4096,memory,0xe0000060,0x4000),('.boot',0x5000,bytes(b),0x60000060,0)],64,0x5000)
if __name__=='__main__':
    for k in ['positive','wrong-call','wrong-variable','no-gate','no-load']:(ROOT/('clr-'+k+'.exe')).write_bytes(native(k))
    for k in ['positive','no-depacker','file-backed-code']:(ROOT/('aplib-'+k+'.exe')).write_bytes(bootstrap(k))
    for k,level in [('admin','requireAdministrator'),('invoker','asInvoker')]:
        manifest=("<requestedExecutionLevel level='"+level+"' uiAccess='false'/>").encode()
        (ROOT/('manifest-'+k+'.exe')).write_bytes(pe([('.text',4096,b'\xc3',0x60000020,0),('.rsrc',8192,manifest+b'\0SHELL32.dll\0',0x40000040,0)],extra_size=1049088))
