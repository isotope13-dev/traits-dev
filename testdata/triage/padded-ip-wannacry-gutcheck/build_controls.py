"""Generate inert resource-entry fixtures; each entry immediately returns."""
from pathlib import Path
import struct

OUT = Path(__file__).parent
VALIDATE = bytes.fromhex('FF 73 3C 59 81 E9 FD FF FF 7F 81 D9 E6 13 00 00 FF B4 19 E4 13 00 80 66 81 44 24 FC B0 BA')
# Junk instructions between the arithmetic and pointer updates are permitted.
HASH = bytes.fromhex('6B C0 0F 0F B6 4E 03 4B 83 EE EE 2B C1 08 DF 87 DB 8D 76 EF 86 EF 80 7E 03 0A')

def build(name, validation=True, hashing=True, entry=True, executable=True):
    data = bytearray(0x11400)
    def w(off, fmt, *args):
        struct.pack_into('<'+fmt,data,off,*args)
    data[:2]=b'MZ';w(0x3c,'I',0x80);data[0x80:0x84]=b'PE\0\0'
    w(0x84,'HHIIIHH',0x14c,2,0,0,0,224,0x102)
    opt=0x98;w(opt,'H',0x10b);w(opt+16,'III',0x2000 if entry else 0x1000,0x1000,0x2000)
    w(opt+28,'III',0x400000,0x1000,0x200);w(opt+40,'HH',4,0);w(opt+56,'II',0x13000,0x400)
    w(opt+68,'H',3);w(opt+72,'IIII',0x100000,0x1000,0x100000,0x1000);w(opt+92,'I',16)
    for i,(label,va,raw,size,flags) in enumerate([
        (b'.text',0x1000,0x400,0x1000,0x60000020),
        (b'.rsrc',0x2000,0x1400,0x10000,0xe0000060 if executable else 0x40000040),
    ]):
        w(opt+224+i*40,'8sIIIIIIHHI',label,size,va,size,raw,0,0,0,0,flags)
    data[0x400]=data[0x1400]=0xc3
    for off,fragment in [(0x1800,VALIDATE if validation else b''),(0x1c00,HASH if hashing else b'')]:
        data[off:off+len(fragment)]=fragment
    (OUT/name).write_bytes(data)

build('resource-entry-signatures.exe')
build('resource-entry-no-hash.exe',hashing=False)
build('resource-entry-no-validation.exe',validation=False)
build('resource-signatures-unused.exe',entry=False)
build('resource-entry-readonly.exe',executable=False)
