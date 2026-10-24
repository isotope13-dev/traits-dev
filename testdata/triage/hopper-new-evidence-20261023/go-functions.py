from pathlib import Path
import pefile,struct,json,capstone
r=Path('/tmp/hopper-new-review-20261023');inv=json.load(open(r/'inventory.json'))
for sha in ['a58c639a1083','a5d4f63e443a','744f82adda79','d0d3361a56e2','608a6ff026a9']:
 i=next(i for i in inv if i['sha256'].startswith(sha));b=Path(i['path']).read_bytes();pe=pefile.PE(data=b);is64=pe.PE_TYPE==0x20b;psz=8 if is64 else 4;fmt='Q' if is64 else 'I';fs=[]
 for at in range(len(b)):
  if b[at:at+4] not in [bytes.fromhex('f1ffffff'),bytes.fromhex('f0ffffff')]:continue
  if b[at+4:at+8] not in [b'\0\0\x01\x08',b'\0\0\x01\x04']:continue
  try:
   fields=struct.unpack_from('<'+fmt*8,b,at+8);nfunc,nfiles,text,fn,cu,ft,pc,pcln=fields
   if not 1<nfunc<100000:continue
   for j in range(nfunc):
    entry,fo=struct.unpack_from('<II',b,at+pcln+8*j);no=struct.unpack_from('<i',b,at+pcln+fo+4)[0];start=at+fn+no;end=b.index(b'\0',start);name=b[start:end].decode();fs.append({'va':text+entry,'name':name})
   break
  except Exception as e:fs=[]
 if not fs:print('NO PCLN',sha);continue
 out=r/'native'/sha;(out/'go-functions.json').write_text(json.dumps(fs,indent=2)+'\n');by={f['va']:f['name'] for f in fs};cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64 if is64 else capstone.CS_MODE_32);lines=[]
 for j,f in enumerate(fs):
  if not f['name'].startswith('main.'):continue
  end=fs[j+1]['va'] if j+1<len(fs) else f['va']+1024
  if end-f['va']>300000:continue
  try:off=pe.get_offset_from_rva(f['va']-pe.OPTIONAL_HEADER.ImageBase)
  except:continue
  lines.append(f"\nFUNCTION {f['name']} {f['va']:#x} size={end-f['va']}")
  for x in cs.disasm(b[off:off+end-f['va']],f['va']):
   label=''
   if x.mnemonic in ['call','jmp'] and x.op_str.startswith('0x'):label=by.get(int(x.op_str,16),'')
   lines.append(f'{x.address:#x} {x.mnemonic} {x.op_str} {label}')
 (out/'main-asm.txt').write_text('\n'.join(lines));print(sha,'functions',len(fs),'main',sum(f['name'].startswith('main.') for f in fs),flush=True)
