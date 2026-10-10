"""Generate inert PE import/overlay controls; entry point is a single RET."""
import hashlib, json, struct
from pathlib import Path
ROOT = Path(__file__).parent

def image(imports=True, overlay=True, rwx=True):
    data = bytearray(0x1600)
    data[:2] = b'MZ'
    struct.pack_into('<I',data,0x3c,0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH',data,0x84,0x14c,3,1600000000,0,0,224,0x102)
    opt=0x98
    struct.pack_into('<H',data,opt,0x10b)
    data[opt+2]=14
    for off,val in {4:512,8:4096,16:0x1000,20:0x1000,24:0x2000,28:0x400000,32:0x1000,36:0x200,56:0x5000,60:0x200,72:0x100000,76:0x1000,80:0x100000,84:0x1000,92:16}.items():
        struct.pack_into('<I',data,opt+off,val)
    struct.pack_into('<HH',data,opt+40,6,0)
    struct.pack_into('<HH',data,opt+48,6,0)
    struct.pack_into('<H',data,opt+68,3)
    if imports:struct.pack_into('<II',data,opt+104,0x2000,40)
    sec=opt+224
    for i,(name,vs,rva,size,raw,flags) in enumerate([
        (b'.text',512,0x1000,512,0x200,0x60000020),
        (b'.idata',512,0x2000,512,0x400,0xc0000040),
        (b'.rsrc',0x2000,0x3000,4096,0x600,0xe0000040 if rwx else 0x40000040)]):
        struct.pack_into('<8sIIIIIIHHI',data,sec+40*i,name,vs,rva,size,raw,0,0,0,0,flags)
    data[0x200]=0xc3
    if imports:
        names=['GetModuleFileNameA','GetModuleFileNameW','CreateFileA','ReadFile','SetFilePointer','fopen','fread','ftell']
        struct.pack_into('<IIIII',data,0x400,0x2040,0,0,0x20c0,0x2080)
        data[0x4c0:0x4cd]=b'KERNEL32.dll\0'
        pos=0x500
        for i,name in enumerate(names):
            pos=(pos+1)&~1
            encoded=b'\0\0'+name.encode()+b'\0'
            struct.pack_into('<I',data,0x440+4*i,0x2000+pos-0x400)
            struct.pack_into('<I',data,0x480+4*i,0x2000+pos-0x400)
            data[pos:pos+len(encoded)]=encoded
            pos+=len(encoded)
    if overlay:
        data.extend(b''.join(hashlib.sha256(str(i).encode()).digest() for i in range(2200)))
    return bytes(data)

if __name__=='__main__':
    for name,kwargs in [
        ('pe-imports-overlay.exe',{}),
        ('pe-imports-no-overlay.exe',{'overlay':False}),
        ('pe-overlay-no-imports.exe',{'imports':False}),
        ('pe-readonly-rsrc.exe',{'rwx':False})]:
        (ROOT/name).write_bytes(image(**kwargs))
