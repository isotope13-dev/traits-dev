"""Generate inert ELF controls; these files have no executable program headers."""
import struct
from pathlib import Path
root=Path(__file__).parent

def elf(name, strings, imports=(), exports=()):
    shstr=b'\0.shstrtab\0.rodata\0.dynstr\0.dynsym\0.text\0'
    dynstr=b'\0';syms=[bytes(24)]
    for symbol in imports:
        offset=len(dynstr);dynstr+=symbol.encode()+b'\0'
        syms.append(struct.pack('<IBBHQQ',offset,0x12,0,0,0,0))
    for symbol in exports:
        offset=len(dynstr);dynstr+=symbol.encode()+b'\0'
        syms.append(struct.pack('<IBBHQQ',offset,0x12,0,5,0x1000,1))
    chunks=[shstr, b'\0'.join(s.encode() for s in strings)+b'\0',dynstr,b''.join(syms),b'\xc3']
    blob=bytearray(bytes(64));sections=[bytes(64)]
    for i,(s,data) in enumerate(zip(['.shstrtab','.rodata','.dynstr','.dynsym','.text'],chunks),1):
        while len(blob)%8:blob.append(0)
        off=len(blob);blob+=data
        kind=11 if i==4 else 3 if i in (1,3) else 1
        flags=6 if i==5 else 2 if i in (2,3,4) else 0
        sections.append(struct.pack('<IIQQQQIIQQ',shstr.index(s.encode()),kind,flags,0x1000 if i==5 else off,off,len(data),3 if i==4 else 0,1 if i==4 else 0,8,24 if i==4 else 0))
    while len(blob)%8:blob.append(0)
    shoff=len(blob);blob+=b''.join(sections)
    blob[:64]=struct.pack('<16sHHIQQQIHHHHHH',b'\x7fELF\x02\x01\x01'+bytes(9),3,62,1,0,0,shoff,0,64,0,0,64,6,1)
    (root/name).write_bytes(blob)

elf('neutral-gecko.so', ['should_hide','/proc/%d/stat','Microsoft Basic Render Driver','TURN to RELAY (%s)','downloadModel','browser.bookmarks.showMobileBookmarks','security.sandbox.content.write_path_whitelist','/tmp/.X11-unix/X','Flush port not found: %s','STOP_ALL','/build/neqo-transport/src/connection/params.rs','Cannot use canvas as context is lost forever.'],['readdir','dlsym','write'],['XRE_main'])
elf('rootkit-filter.so',['original_readdir','/proc/%d/stat'],['readdir','dlsym','write'],['should_hide'])
elf('visibility-predicate.so',['/proc/%d/stat'],['readdir','dlsym','write'],['should_hide'])
elf('hidden-port-actions.so',['list_hidden port','flush_hidden tcp'])
elf('ransom-threat.so',['Your files will be lost forever'])
elf('download-module.so',['main.downloadMod'])
