# Isolated CPU emulation. Every Windows import is an inert mock; no sample
# instruction runs as native host code and no requested OS action is forwarded.
from pathlib import Path
import json,struct,pefile,time,hashlib,hmac
import unicorn
from unicorn.x86_const import *
rows=[{'sha256':'rebrrgb-stage2','local_path':'/tmp/endpoint-review-20261023/native/6d6a677eea21/mapped-0x801a4000-rebuilt.dll'}]
for row in rows:
 if False:continue
 p=pefile.PE(row['local_path']);base=p.OPTIONAL_HEADER.ImageBase
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(base,(p.OPTIONAL_HEADER.SizeOfImage+4095)&~4095);u.mem_write(base,p.get_memory_mapped_image())
 for addr,size in [(0x50000000,0x200000),(0x51000000,0x200000),(0x60000000,0x100000),(0x70000000,0x1000000),(0x80000000,0x4000000)]:u.mem_map(addr,size)
 u.reg_write(UC_X86_REG_GS_BASE,0x50000000);u.mem_write(0x50000058,struct.pack('<Q',0x50001000));u.mem_write(0x50001000,struct.pack('<Q',0x50002000))
 u.mem_write(0x50000060,struct.pack('<Q',0x50010000));u.mem_write(0x50010010,struct.pack('<Q',base));u.mem_write(0x50010018,struct.pack('<Q',0x50011000));u.mem_write(0x50010110,struct.pack('<Q',0x50012000))
 for off in [0x10,0x20,0x30]:u.mem_write(0x50011000+off,struct.pack('<QQ',0x50011000+off,0x50011000+off))
 if hasattr(p,'DIRECTORY_ENTRY_TLS'):
  t=p.DIRECTORY_ENTRY_TLS.struct;u.mem_write(0x50002000,p.get_data(t.StartAddressOfRawData-base,t.EndAddressOfRawData-t.StartAddressOfRawData))
 imports={};byname={};events=[];threads=[];cursor=0x80001000;allocs={};stopped=[];fls={};hashes={}
 def stub(name):
  if name not in byname:
   a=0x60000000+len(byname)*16;byname[name]=a;imports[a]=name
  return byname[name]
 for d in p.DIRECTORY_ENTRY_IMPORT:
  for x in d.imports:u.mem_write(x.address,struct.pack('<Q',stub(x.name.decode() if x.name else '#'+str(x.ordinal))))
 def readstr(addr,wide=False):
  try:
   b=bytes(u.mem_read(addr,1024));return b.decode('utf-16le',errors='replace').split('\0')[0] if wide else b.split(b'\0')[0].decode(errors='replace')
  except:return '<unmapped>'
 def alloc(n):
  global cursor
  if n<0 or n>0x1000000:raise RuntimeError('allocation bound')
  addr=cursor;cursor+=(n+4095)&~4095
  if cursor>=0x84000000:raise RuntimeError('heap bound')
  allocs[addr]=n;return addr
 class Stop(Exception):pass
 def api(u,a,size,data):
  name=imports.get(a)
  if name is None:return
  args=[u.reg_read(r) for r in [UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9]];sp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(sp,8))[0];result=0
  e={'api':name,'caller':hex(ret),'args':[hex(x) for x in args]};events.append(e)
  if len(events)>3000:raise Stop('API event bound')
  if name=='GetProcAddress':e['name']=readstr(args[1]);result=stub(e['name'])
  elif name.startswith(('LoadLibrary','GetModuleHandle')):e['name']=readstr(args[0],name.endswith('W'));result=0x51000000
  elif name in ['GetProcessHeap']:result=1
  elif name in ['HeapAlloc','LocalAlloc','VirtualAlloc']:result=alloc(args[2] if name=='HeapAlloc' else args[1])
  elif name=='HeapReAlloc':
   result=alloc(args[3]);u.mem_write(result,bytes(u.mem_read(args[2],min(args[3],allocs.get(args[2],0)))))
  elif name in ['HeapSize']:result=allocs.get(args[2],0)
  elif name in ['GetCurrentThreadId','GetCurrentProcessId','GetThreadId']:result=1000
  elif name=='GetCurrentProcess':result=0xffffffffffffffff
  elif name=='GetCurrentThread':result=0xfffffffffffffffe
  elif name=='TlsAlloc' or name=='FlsAlloc':result=1
  elif name in ['TlsGetValue','FlsGetValue','FlsGetValue2']:result=fls.get(args[0],0)
  elif name=='TlsSetValue' or name=='FlsSetValue':fls[args[0]]=args[1];result=1
  elif name=='EncodePointer' or name=='DecodePointer':result=args[0]
  elif name in ['HeapFree','CloseHandle','FreeLibrary','InitializeCriticalSectionEx','TlsFree','FlsFree','SetWaitableTimer','FlushFileBuffers']:result=1
  elif name in ['GetSystemTimeAsFileTime','QueryPerformanceCounter','QueryPerformanceFrequency']:
   u.mem_write(args[0],struct.pack('<Q',123456789));result=1
  elif name in ['GetTickCount','GetTickCount64']:result=123456789
  elif name in ['GetSystemInfo','GetNativeSystemInfo']:
   u.mem_write(args[0],b'\0'*48);u.mem_write(args[0]+32,struct.pack('<I',8))
  elif name=='GlobalMemoryStatusEx':
   u.mem_write(args[0],struct.pack('<II7Q',64,30,16<<30,8<<30,32<<30,16<<30,1<<40,1<<39,0));result=1
  elif name=='GetModuleFileNameW':
   t='C:\\Program Files\\Windows Defender\\MsMpEng.exe\0';u.mem_write(args[1],t.encode('utf-16le'));result=len(t)-1
  elif name in ['GetCommandLineW','GetCommandLineA']:
   text='C:\\Analysis\\sample.exe\0';addr=alloc(200);u.mem_write(addr,text.encode('utf-16le') if name.endswith('W') else text.encode());result=addr
  elif name=='GetEnvironmentStringsW':addr=alloc(16);u.mem_write(addr,b'\0'*8);result=addr
  elif name=='GetLastError':result=0
  elif name in ['IsDebuggerPresent','IsProcessorFeaturePresent','GetActiveWindow','GetForegroundWindow','GetDesktopWindow','IsWindowVisible','IsIconic']:result=0
  elif name in ['VirtualProtect']:u.mem_write(args[3],struct.pack('<I',0x20));result=1
  elif name=='CreateThread':
   e['entry']=hex(args[2]);e['parameter']=hex(args[3]);threads.append((args[2],args[3]));result=0x99
  elif name in ['GetStdHandle']:result=0x98
  elif name in ['GetConsoleMode','GetFileType']:result=0
  elif name in ['CreateWaitableTimerExW']:result=0x97
  elif name in ['Sleep','WaitForSingleObject','WaitOnAddress']:result=0
  elif name in ['WriteFile','WriteConsoleW']:e['text']=readstr(args[1],name.endswith('W'));result=1
  elif name=='EnumDisplayDevicesW':
   if args[1]==0:
    u.mem_write(args[2]+4,'DISPLAY1\0'.encode('utf-16le'));u.mem_write(args[2]+68,'NVIDIA GeForce RTX\0'.encode('utf-16le'));result=1
   else:result=0
  elif name in ['LCMapStringEx','LCMapStringW']:
   dst,n=struct.unpack('<QQ',u.mem_read(sp+0x28,16));raw=bytes(u.mem_read(args[2],args[3]*2));text=raw.decode('utf-16le',errors='replace');out=(text.lower() if args[1]&0x100 else text.upper()).encode('utf-16le');result=len(out)//2
   if dst and n>=result:u.mem_write(dst,out)
  elif name=='SetProcessDPIAware':result=1
  elif name=='GetSystemMetrics':result=1920 if args[0]==0 else 1080 if args[0]==1 else 1
  elif name=='GetStringTypeW':
   u.mem_write(args[3],b'\0'*(min(args[2],4096)*2));result=1
  elif name=='RtlGetVersion':
   u.mem_write(args[0],struct.pack('<5I',276,10,0,19045,2)+b'\0'*256);result=0
  elif name=='BCryptOpenAlgorithmProvider':
   e['algorithm']=readstr(args[1],True);u.mem_write(args[0],struct.pack('<Q',0xa1));result=0
  elif name=='BCryptCreateHash':
   hp=0xa200+len(hashes)*16;hashes[hp]=bytearray();u.mem_write(args[1],struct.pack('<Q',hp));result=0
  elif name=='BCryptHashData':
   hashes[args[0]].extend(u.mem_read(args[1],min(args[2],1<<20)));e['input_hex']=bytes(u.mem_read(args[1],min(args[2],1000))).hex();result=0
  elif name=='BCryptFinishHash':
   digest=hashlib.sha256(hashes[args[0]]).digest();u.mem_write(args[1],digest[:args[2]]);result=0
  elif name in ['BCryptDestroyHash','BCryptCloseAlgorithmProvider']:result=0
  elif name in ['WinHttpSetTimeouts','WinHttpSetOption']:result=1
  elif name in ['RtlEnterCriticalSection','RtlLeaveCriticalSection']:result=0
  elif name=='WinHttpOpen':e['agent']=readstr(args[0],True);result=0x111
  elif name=='WinHttpConnect':e['server']=readstr(args[1],True);e['port']=args[2]&0xffff;result=0x112
  elif name=='WinHttpOpenRequest':e['verb']=readstr(args[1],True);e['path']=readstr(args[2],True);result=0x113
  elif name=='WinHttpSendRequest':
   e['headers']=readstr(args[1],True);n=qword=struct.unpack('<Q',u.mem_read(sp+0x28,8))[0];e['body_hex']=bytes(u.mem_read(args[3],min(n,100000))).hex() if args[3] else '';result=1
  elif name=='WinHttpWriteData':e['data_hex']=bytes(u.mem_read(args[1],min(args[2],100000))).hex();raise Stop('captured HTTP body without network')
  elif name=='RtlGetCurrentPeb':result=0x50010000
  elif name=='GetDriveTypeW':result=3
  elif name=='GetFileAttributesW':e['path']=readstr(args[0],True);result=0xffffffff
  elif name=='GetLogicalDrives':result=4
  elif name=='RegOpenKeyExW':
   e['path']=readstr(args[1],True);result=2
  elif name=='GetSystemFirmwareTable':e['provider']=hex(args[0]);result=0
  elif name=='IsThreadAFiber':result=0
  elif name=='AreFileApisANSI':result=1
  elif name=='GetUserNameW':
   text='employee';u.mem_write(args[0],(text+'\0').encode('utf-16le'));u.mem_write(args[1],struct.pack('<I',len(text)+1));result=1
  elif name=='GetComputerNameW':
   text='CORP-USER-PC';u.mem_write(args[0],(text+'\0').encode('utf-16le'));u.mem_write(args[1],struct.pack('<I',len(text)));result=1
  elif name=='MultiByteToWideChar':
   dst,n=struct.unpack('<QQ',u.mem_read(sp+0x28,16));n0=args[3]&0xffffffff;raw=bytes(u.mem_read(args[2],n0)) if n0!=0xffffffff else readstr(args[2]).encode()+b'\0';out=raw.decode('cp1252',errors='replace').encode('utf-16le');result=len(out)//2
   if dst and n>=result:u.mem_write(dst,out)
  elif name=='WideCharToMultiByte':
   dst,n=struct.unpack('<QQ',u.mem_read(sp+0x28,16));n0=args[3]&0xffffffff;raw=bytes(u.mem_read(args[2],n0*2)) if n0!=0xffffffff else (readstr(args[2],True)+'\0').encode('utf-16le');out=raw.decode('utf-16le',errors='replace').encode('cp1252',errors='replace');result=len(out)
   if dst and n>=result:u.mem_write(dst,out)
  elif name=='GetUserDefaultLocaleName':
   u.mem_write(args[0],'en-US\0'.encode('utf-16le'));result=6
  elif name=='IsValidCodePage':result=1
  elif name=='GetCPInfo':u.mem_write(args[1],struct.pack('<I',1)+b'\0'*16);result=1
  elif name=='GetStartupInfoW':u.mem_write(args[0],b'\0'*104)
  elif name=='GetVolumeInformationW':
   u.mem_write(args[3],struct.pack('<I',0x12345678));result=1
  elif name in ['GetACP','GetOEMCP','GetConsoleCP','GetConsoleOutputCP']:result=1252
  elif name in ['ExitProcess','TerminateProcess']:raise Stop(name)
  elif name in ['EnterCriticalSection','LeaveCriticalSection','DeleteCriticalSection','InitializeSListHead','SetLastError','WakeByAddressAll','WakeByAddressSingle','SetUnhandledExceptionFilter','FreeEnvironmentStringsW']:pass
  else:e['strings']=[readstr(x) for x in args];e['wide']=[readstr(x,True) for x in args];raise Stop('unimplemented '+name)
  u.reg_write(UC_X86_REG_RAX,result);u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RIP,ret)
 u.hook_add(unicorn.UC_HOOK_CODE,api,begin=0x60000000,end=0x600fffff)
 def syscall(u,user):raise Stop('syscall intercepted')
 u.hook_add(unicorn.UC_HOOK_INSN,syscall,None,1,0,UC_X86_INS_SYSCALL)
 def run(entry,arg=0,dll=False):
  sp=0x70f00008;end=0x600ff000;u.mem_write(sp,struct.pack('<Q',end));u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RCX,base if dll else arg);u.reg_write(UC_X86_REG_RDX,1 if dll else 0);u.reg_write(UC_X86_REG_R8,0);u.reg_write(UC_X86_REG_R9,0)
  start=time.monotonic()
  try:u.emu_start(entry,end,timeout=15000000,count=400000000);why='return or CPU bound'
  except (Stop,unicorn.UcError,RuntimeError) as e:why=str(e)
  stopped.append({'entry':hex(entry),'pc':hex(u.reg_read(UC_X86_REG_RIP)),'reason':why,'seconds':time.monotonic()-start,'return':hex(u.reg_read(UC_X86_REG_RAX))})
 run(base+p.OPTIONAL_HEADER.AddressOfEntryPoint,dll=bool(p.FILE_HEADER.Characteristics&0x2000))
 for entry,arg in threads[:3]:run(entry,arg)
 if row['sha256'].startswith('6d6a'):
  for ex in p.DIRECTORY_ENTRY_EXPORT.symbols:
   if ex.name and ex.name.decode() in ['MpClientUtilExportFunctions','MpManagerOpen','MpManagerVersionQuery','MpScanStart','MpAllocMemory']:
    events.append({'export':ex.name.decode()});run(base+ex.address)
 root=Path('/tmp/endpoint-review-20261023/native')/row['sha256'][:12];root.mkdir(exist_ok=True)
 for address,n in allocs.items():
  if n>=65536:
   blob=bytes(u.mem_read(address,n))
   if blob[:2]==b'MZ':
    path=root/('mapped-'+hex(address)+'.bin');path.write_bytes(blob);events.append({'mapped_capture':str(path),'size':n})
 (root/'emulation.json').write_text(json.dumps({'events':events,'stops':stopped,'threads':threads},indent=2));print(row['sha256'][:12],json.dumps(stopped), 'events',len(events),'threads',threads,flush=True)
