from pathlib import Path
import pefile,capstone,hashlib,json,re,collections
r=Path('/tmp/hopper-new-review-20261023');inv=json.load(open(r/'inventory.json'));summ=[]
for i in inv:
 p=Path(i['path']);b=p.read_bytes()
 if not b.startswith(b'MZ'):continue
 out=r/'native'/i['sha256'][:12];out.mkdir(parents=True,exist_ok=True)
 try:pe=pefile.PE(data=b)
 except Exception as e:print(e);continue
 entry=pe.OPTIONAL_HEADER.ImageBase+pe.OPTIONAL_HEADER.AddressOfEntryPoint;start=pe.get_offset_from_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64 if pe.PE_TYPE==0x20b else capstone.CS_MODE_32)
 asm=[f'{x.address:#x} {x.mnemonic} {x.op_str}' for x in cs.disasm(b[start:start+700],entry)]
 imports=[x.dll.decode(errors='replace')+':'+(f.name.decode(errors='replace') if f.name else '#'+str(f.ordinal)) for x in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]) for f in x.imports]
 versions=[]
 for fi in getattr(pe,'FileInfo',[]):
  for z in fi:
   for tb in getattr(z,'StringTable',[]):versions.append({k.decode(errors='replace'):v.decode(errors='replace') for k,v in tb.entries.items()})
 resources=[]
 def walk(node,parts=[]):
  for x in node.entries:
   name=str(x.name) if x.name else str(x.struct.Id)
   if hasattr(x,'directory'):walk(x.directory,parts+[name])
   elif hasattr(x,'data'):
    data=pe.get_data(x.data.struct.OffsetToData,x.data.struct.Size);f=out/('resource-'+'-'.join(parts+[name])+'.bin');f.write_bytes(data);resources.append({'path':'/'.join(parts+[name]),'file':str(f),'rva':x.data.struct.OffsetToData,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'magic':data[:12].hex()})
 if hasattr(pe,'DIRECTORY_ENTRY_RESOURCE'):walk(pe.DIRECTORY_ENTRY_RESOURCE)
 ss=[{'name':s.Name.rstrip(b'\0').decode(errors='replace'),'rva':s.VirtualAddress,'raw_offset':s.PointerToRawData,'raw_size':s.SizeOfRawData,'virtual_size':s.Misc_VirtualSize,'entropy':s.get_entropy(),'flags':hex(s.Characteristics)} for s in pe.sections]
 strings=[x.decode(errors='replace') for x in re.findall(rb'[\x20-\x7e]{5,}',b)];wide=[x.decode('utf-16le',errors='replace') for x in re.findall(rb'(?:[\x20-\x7e]\0){5,}',b)]
 (out/'strings.txt').write_text('\n'.join(strings+wide))
 d={'path':str(p),'sha256':i['sha256'],'entry':hex(entry),'entry_file_offset':start,'sections':ss,'versions':versions,'imports':imports,'resources':resources,'entry_disassembly':asm,'security_directory':{'offset':pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].VirtualAddress,'size':pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size}}
 (out/'structure.json').write_text(json.dumps(d,indent=2)+'\n');summ.append(d)
 print(i['sha256'][:12],p.name[:40],versions,[(s['name'],round(s['entropy'],2)) for s in ss],len(resources),flush=True)
(r/'native-summary.json').write_text(json.dumps(summ,indent=2)+'\n')
