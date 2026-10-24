from pathlib import Path
import json,struct,hashlib,re
import pefile,capstone
p=Path('/tmp/triage-good-20261024');r=json.loads((p/'inventory.json').read_text())[63];pe=pefile.PE(r['path']);base=pe.OPTIONAL_HEADER.ImageBase;image=(p/'native/63/emulated-image.bin').read_bytes();sec=pe.sections[-1];end=sec.VirtualAddress+sec.SizeOfRawData
key=image[end-0x28:end-0x20];length=struct.unpack_from('<I',image,end-0xc)[0];rva=struct.unpack_from('<I',image,end-8)[0];oep=struct.unpack_from('<I',image,end-0x1c)[0];print('end',hex(end),'key',key.hex(),'len',length,'rva',hex(rva),'oep',hex(oep))
assert 0<length<10000000 and rva+length<=len(image)
s=list(range(256));j=0
for x in range(256):j=(j+s[x]+key[x%8])%256;s[x],s[j]=s[j],s[x]
a=j=0;out=bytearray()
for v in image[rva:rva+length]:
 a=(a+1)%256;j=(j+s[a])%256;s[a],s[j]=s[j],s[a];out.append(v^s[(s[a]+s[j])%256])
(p/'native/63/payload.dll').write_bytes(out);print('payload',out[:16].hex(),hashlib.sha256(out).hexdigest());child=pefile.PE(data=out);report={'outer_sha256':r['sha256'],'initial_decoder':{'va':hex(0x5264ea),'xor':0x5f,'length':0x47,'next_stage':hex(0x5ca4c4)},'resource_loader':{'entry':hex(0x5cd967),'rc4_key':key.hex(),'payload_rva':hex(rva),'payload_size':length,'host_original_entry_rva':hex(oep),'activation':'Manual maps RC4-decoded DLL, applies HIGHLOW relocations, resolves imports, calls DLL entry with DLL_PROCESS_ATTACH, then returns to the saved host entry.'},'payload':{'sha256':hashlib.sha256(out).hexdigest(),'size':len(out),'dll':bool(child.FILE_HEADER.Characteristics&0x2000),'entry_rva':hex(child.OPTIONAL_HEADER.AddressOfEntryPoint),'imports':{x.dll.decode():[(i.name.decode() if i.name else '#'+str(i.ordinal)) for i in x.imports] for x in getattr(child,'DIRECTORY_ENTRY_IMPORT',[])},'exports':[(x.name.decode() if x.name else '#'+str(x.ordinal)) for x in getattr(child,'DIRECTORY_ENTRY_EXPORT',type('E',(),{'symbols':[]})()).symbols]}}
(p/'native/63/recovery.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['payload'],indent=2))
