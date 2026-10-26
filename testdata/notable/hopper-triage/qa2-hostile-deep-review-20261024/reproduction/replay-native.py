"""Bounded emulation of reviewed main; every call is a synthetic data stub.
No Windows/library implementation or application-generated copy is executed.
"""
from pathlib import Path
import json,struct,hashlib
import pefile,capstone
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_INVALID
from unicorn.x86_const import *
base=Path('/tmp/qa2-deep-review');recovery=json.load(open(base/'native/recovery.json'));samples=[{'original_path':str(next(Path('/tmp/qa2/hostile').glob('aab*/*'))),'recovered_path':str(next(Path('/tmp/qa2/hostile').glob('aab*/*')))}]+recovery
results=[]
for sample in samples:
 original=Path(sample['original_path']).read_bytes();image=Path(sample['recovered_path']).read_bytes();pe=pefile.PE(data=image);b=pe.OPTIONAL_HEADER.ImageBase
 imports={i.address:i.name.decode() for d in pe.DIRECTORY_ENTRY_IMPORT for i in d.imports if i.name};exports={b+s.address:s.name.decode() for s in pe.DIRECTORY_ENTRY_EXPORT.symbols if s.name}
 for remove_marker in [False,True]:
  content=original.replace(b'[[UNIQUE]]',b'[[ABSENT]]') if remove_marker else original
  u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(b,0x30000);u.mem_write(b,pe.get_memory_mapped_image());u.mem_map(0x20000000,0x200000);u.mem_map(0x30000000,0x400000);u.mem_map(0x70000000,0x200000)
  def read32(a):return struct.unpack('<I',u.mem_read(a,4))[0]
  def write32(a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
  def string(a):
   if not a:return ''
   out=bytearray()
   for i in range(4096):
    c=bytes(u.mem_read(a+i,1))
    if c==b'\0':return out.decode('latin1')
    out.extend(c)
   raise AssertionError('Unbounded string')
  u.mem_write(0x20000100,b'C:\\Synthetic\\sample.exe\0');write32(0x20000000,0x20000100)
  sp=0x70100000;u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_EBP,sp+0x1000)
  for i,v in enumerate([0x70001000,1,0x20000000,0]):write32(sp+i*4,v)
  events=[];disk={};handles={};counter=[0];sleep_count=[0];stop=[]
  md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
  def invoke(name,args):
   events.append({'operation':name,'arguments':args[:5]})
   if name=='GetModuleFileNameA':u.mem_write(args[1],b'C:\\Synthetic\\sample.exe\0');return 23,12
   if name=='fopen':
    path=string(args[0]);mode=string(args[1]);h=len(handles)+0x100;handles[h]=(path,mode);events[-1].update(path=path,mode=mode);return h,0
   if name=='fseek':return 0,0
   if name=='ftell':return len(content),0
   if name=='malloc':return 0x30000000,0
   if name=='fread':u.mem_write(args[0],content[:args[1]*args[2]]);return len(content)//args[1],0
   if name in ['fclose','srand','curl_global_init','curl_easy_cleanup','curl_formfree','curl_global_cleanup']:return 0,0
   if name=='time':return 1700000000,0
   if name=='rand':counter[0]+=1;return (counter[0]*31+7)%32768,0
   if name=='memcmp':return (bytes(u.mem_read(args[0],args[2]))>bytes(u.mem_read(args[1],args[2])))-(bytes(u.mem_read(args[0],args[2]))<bytes(u.mem_read(args[1],args[2]))),0
   if name=='puts':events[-1]['text']=string(args[0]);return 0,0
   if name=='printf':events[-1]['format']=string(args[0]);return 0,0
   if name=='sprintf':
    fmt=string(args[1]);value=string(args[2]) if '%s' in fmt else args[2];s=(fmt.replace('%i','%d')%value).encode()+b'\0';u.mem_write(args[0],s);events[-1]['result']=s[:-1].decode();return len(s)-1,0
   if name=='Sleep':
    sleep_count[0]+=1
    if sleep_count[0]>1:stop.append('one complete loop; next delay reached');u.emu_stop()
    return 0,4
   if name=='fwrite':
    path,mode=handles[args[3]];data=bytes(u.mem_read(args[0],args[1]*args[2]));disk[path]=data;diff=[i for i,(x,y) in enumerate(zip(content,data)) if x!=y];events[-1].update(path=path,size=len(data),clone_sha256=hashlib.sha256(data).hexdigest(),changed_offsets=diff);return args[2],0
   if name=='curl_formadd':
    write32(args[0],0x30300000);write32(args[1],0x30300020);events[-1].update(field=string(args[3]),value=string(args[5]) if len(args)>5 else '');return 0,0
   if name=='curl_easy_init':return 0xcafe,0
   if name=='curl_easy_setopt':events[-1].update(option=args[1],value=string(args[2]) if args[1]==10002 else args[2]);return 0,0
   if name=='curl_easy_perform':return 0,0
   if name=='_unlink':events[-1]['path']=string(args[0]);return 0,0
   raise AssertionError('Unexpected reviewed call '+name)
  def hook(uc,at,size,user):
   if not 0x4013a0<=at<0x4016e2:stop.append('outside reviewed main at '+hex(at));uc.emu_stop();return
   if at==0x40146e:
    # Summarize only the reviewed bounded memcmp marker-search loop.
    found=content.find(b'[[UNIQUE]]')
    events.append({'operation':'bounded-marker-search','offset':found})
    if found>=0 and found<len(content)-10:
     write32(0x423030,found+10);uc.reg_write(UC_X86_REG_EAX,0);uc.reg_write(UC_X86_REG_EBX,found)
    else:uc.reg_write(UC_X86_REG_EAX,1)
    uc.reg_write(UC_X86_REG_EIP,0x40149e);return
   code=bytes(uc.mem_read(at,size))
   if code==b'\x0f\x31':uc.reg_write(UC_X86_REG_EAX,0x12345678);uc.reg_write(UC_X86_REG_EDX,0x23456789);uc.reg_write(UC_X86_REG_EIP,at+size);return
   if code[0]!=0xe8:return
   target=at+5+struct.unpack('<i',code[1:5])[0]
   if target==0x401320:uc.reg_write(UC_X86_REG_EIP,at+size);return
   name=exports.get(target)
   if name is None:
    head=bytes(uc.mem_read(target,6));assert head[:2]==b'\xff\x25',(hex(target),head.hex());name=imports[struct.unpack('<I',head[2:])[0]]
   sp=uc.reg_read(UC_X86_REG_ESP);args=[read32(sp+i*4) for i in range(8)];ret,pop=invoke(name,args);uc.reg_write(UC_X86_REG_EAX,ret&0xffffffff);uc.reg_write(UC_X86_REG_ESP,sp+pop);uc.reg_write(UC_X86_REG_EIP,at+size)
  def badmem(uc,access,at,size,value,user):stop.append('blocked unmapped memory '+hex(at));return False
  u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_INVALID,badmem)
  try:u.emu_start(0x4013a0,0x70001000,count=1_000_000,timeout=3_000_000)
  except UcError as e:stop.append(str(e))
  ops=[e['operation'] for e in events];assert ('curl_easy_perform' in ops)==(not remove_marker),(sample['original_path'],stop,events[-3:])
  if not remove_marker:
   write=next(e for e in events if e['operation']=='fwrite');assert len(write['changed_offsets'])<=16 and len(write['changed_offsets'])>0
   marker=content.index(b'[[UNIQUE]]')+10;assert all(marker<=x<marker+16 for x in write['changed_offsets'])
   assert 'one complete loop; next delay reached' in stop
  results.append({'sample_sha256':hashlib.sha256(original).hexdigest(),'remove_marker_control':remove_marker,'stops':stop,'events':events});print(hashlib.sha256(original).hexdigest()[:12],remove_marker,len(events),'calls',stop)
(base/'native/synthetic-main-replays.json').write_text(json.dumps(results,indent=2)+'\n')
