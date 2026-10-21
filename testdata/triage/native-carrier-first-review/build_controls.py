"""Inert PE matcher controls. The entry point only returns; APIs are never called."""
from pathlib import Path
import struct,json
b=Path(__file__).parent

def pe(strings,imports=('CreateProcessA',),overlay=b''):
    h=bytearray(0x200);h[:2]=b'MZ';struct.pack_into('<I',h,0x3c,0x80);h[0x80:0x84]=b'PE\0\0'
    struct.pack_into('<HHIIIHH',h,0x84,0x14c,2,0,0,0,0xe0,0x102)
    o=0x98;struct.pack_into('<H',h,o,0x10b);struct.pack_into('<III',h,o+4,0x200,0x1000,0)
    struct.pack_into('<III',h,o+16,0x1000,0x1000,0x2000);struct.pack_into('<III',h,o+28,0x400000,0x1000,0x200)
    struct.pack_into('<HHHHHH',h,o+40,4,0,0,0,4,0);struct.pack_into('<III',h,o+56,0x3000,0x200,0);struct.pack_into('<HH',h,o+68,2,0x140)
    struct.pack_into('<IIIIII',h,o+72,0x100000,0x1000,0x100000,0x1000,0,16);struct.pack_into('<II',h,o+104,0x2000,40)
    for i,(name,vs,va,rs,off,flags) in enumerate([(b'.text',1,0x1000,0x200,0x200,0x60000020),(b'.rdata',0x1000,0x2000,0x1000,0x400,0x40000040)]):
        struct.pack_into('<8sIIIIIIHHI',h,o+0xe0+40*i,name,vs,va,rs,off,0,0,0,0,flags)
    code=b'\xc3'+bytes(0x1ff);d=bytearray(0x1000)
    struct.pack_into('<IIIII',d,0,0x2040,0,0,0x20a0,0x2070);d[0xa0:0xad]=b'kernel32.dll\0'
    at=0x100
    for i,n in enumerate(imports):
        struct.pack_into('<I',d,0x40+i*4,0x2000+at);struct.pack_into('<I',d,0x70+i*4,0x2000+at)
        x=b'\0\0'+n.encode()+b'\0';d[at:at+len(x)]=x;at+=len(x)+(len(x)%2)
    s=b'\0'.join(v.encode() for v in strings)+b'\0';assert len(s)<0xb00;d[0x400:0x400+len(s)]=s
    return bytes(h)+code+bytes(d)+overlay

login='{"jsonrpc":"2.0","method":"login","params":{"login":"x"}}'
submit='{"jsonrpc":"2.0","method":"submit","params":{}}'
commands=['cmd /c net stop WinDefend','cmd /c sc config WinDefend start= disabled','net stop SharedAccess','sc config SharedAccess start= disabled']
exploit=['--TargetPort 445 --DllPayload','--DllOrdinal 1 ProcessName target.exe']
for name,raw in {
    'all-behavior-evidence.exe':pe([login]+commands+exploit),
    'mining-only.exe':pe([login,submit,'https://pool.supportxmr.com','aes_256_cbc','HEAD / HTTP/1.0','http://example.icu/','http://example.pw/']),
    'unrelated-services.exe':pe([login,'net start SharedAccess','sc config Spooler start= disabled','net stop Spooler']),
    'overlay-only.exe':pe(['ordinary data'],overlay=('\0'.join([login]+commands+exploit)).encode()),
    'debugger-only.exe':pe(['ordinary debugger'],imports=('DebugActiveProcess','WaitForDebugEvent','ContinueDebugEvent')),
    'missing-dll-payload.exe':pe([login]+commands+exploit[1:]),
}.items():(b/name).write_bytes(raw)
