"""Inert matcher controls, with no live endpoints or payload execution."""
from pathlib import Path
import struct
ROOT=Path(__file__).parent

def elf(payload):
 b=bytearray(0x1000)+b'\xc3'+payload
 b[:16]=b'\x7fELF\x02\x01\x01'+b'\0'*9
 struct.pack_into('<HHIQQQIHHHHHH',b,16,2,62,1,0x401000,64,0,0,64,56,1,0,0,0)
 struct.pack_into('<IIQQQQQQ',b,64,1,5,0,0x400000,0x400000,len(b),len(b),4096)
 return b

# Same buffer is passed through both calls; direct callees are unknown.
# The entry point is RET. These bytes model static call structure only.
layout=bytes.fromhex('49 89 E6 48 89 D9 BA 00 08 00 00 4C 89 F7 BE 01 00 00 00 E8 00 00 00 00 48 89 DF 48 89 C5 E8 00 00 00 00 83 FD 0A 7F 00 48 63 C5 4C 89 F6 4C 89 EF C6 04 04 00 E8 00 00 00 00')
paths=b'\0/root/.ssh/id_rsa\0/root/.bash_history\0'
post=b'\0POST /upload HTTP/1.0\r\nHost: localhost\r\nContent-Length:%d\r\n\r\n%s\0'
for name,body in {
 'buffer-path-post':layout+paths+post,
 'paths-post-only':paths+post,
 'buffer-post-only':layout+post,
 'buffer-path-only':layout+paths,
 'different-buffer':layout.replace(bytes.fromhex('4C 89 F6'),bytes.fromhex('4C 89 E6'))+paths+post,
}.items(): (ROOT/(name+'.elf')).write_bytes(elf(body))

# A normal GUI/resource editor can import every API that the retired
# spyware/resource-infector rules used; its entry point simply returns.
imports=['GetLogicalDriveStringsA','GetDriveTypeA',
 'FindFirstFileA','FindNextFileA','BeginUpdateResourceA','UpdateResourceA',
 'EndUpdateResourceA','BitBlt','GetDIBits','GetDesktopWindow','GetKeyState',
 'GetProcAddress','LoadLibraryA','RegisterClipboardFormatA']
b=bytearray(0x1600);b[:2]=b'MZ';struct.pack_into('<I',b,0x3c,0x80)
b[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',b,0x84,0x14c,3,1600000000,0,0,224,0x102)
o=0x98;struct.pack_into('<H',b,o,0x10b)
for off,val in {4:512,8:4096,16:0x1000,20:0x1000,24:0x2000,28:0x400000,32:0x1000,36:0x200,56:0x4000,60:0x200,72:0x100000,76:0x1000,80:0x100000,84:0x1000,92:16}.items():struct.pack_into('<I',b,o+off,val)
struct.pack_into('<H',b,o+68,3);struct.pack_into('<II',b,o+104,0x2000,40)
for i,(n,rva,raw,size,flags) in enumerate([(b'.text',0x1000,0x200,512,0x60000020),(b'.idata',0x2000,0x400,4096,0xc0000040),(b'.rsrc',0x3000,0x1400,512,0x40000040)]):
 struct.pack_into('<8sIIIIIIHHI',b,o+224+i*40,n,size,rva,size,raw,0,0,0,0,flags)
b[0x200]=0xc3
strings=b'*.exe*\0SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\0'
b[0x220:0x220+len(strings)]=strings
struct.pack_into('<IIIII',b,0x400,0x2040,0,0,0x2100,0x20a0)
b[0x500:0x50d]=b'KERNEL32.dll\0';pos=0x520
for i,n in enumerate(imports):
 pos=(pos+1)&~1;s=b'\0\0'+n.encode()+b'\0';rva=0x2000+pos-0x400
 struct.pack_into('<I',b,0x440+i*4,rva);struct.pack_into('<I',b,0x4a0+i*4,rva)
 b[pos:pos+len(s)]=s;pos+=len(s)
(ROOT/'gui-resource-editor.exe').write_bytes(b)
(ROOT/'router-form.sh').write_text("#!/bin/sh\nbody='wanMTU=1500&mac=00:00:00:00:00:00&serviceName='\n")
(ROOT/'history-pattern.sh').write_text("#!/bin/sh\ngrep -oE 'ssh [^@]+@[0-9.]+' /root/.bash_history\n")
(ROOT/'history-command.sh').write_text('#!/bin/sh\nssh example.invalid cat /root/.bash_history\n')
