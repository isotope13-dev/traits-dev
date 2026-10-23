"""Recover this Foxveil specimen offline with Unicorn and cryptography.

Usage: python3 recover_native.py --sample <original universal Mach-O> --output <dir>
Only CPU instructions run in Unicorn. Every native/OSA/Objective-C API is a Python
stub: there are no specimen-driven host processes, filesystem writes or network
calls. Authentication verifies the selected ordinary-environment key path. The
five anti-analysis predicates are explicitly assumed false for key recovery;
this is not a dynamic observation of an unmodified process. Recovered OSA bytes
are saved, never executed. Unknown APIs stop the emulation.
"""
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--sample',type=__import__('pathlib').Path,required=True);ap.add_argument('--output',type=__import__('pathlib').Path,required=True);opt=ap.parse_args()
import pathlib,struct,sys,hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from unicorn import *
from unicorn.x86_const import *
P=opt.output;P.mkdir(parents=True,exist_ok=True)
original=opt.sample.read_bytes()
assert hashlib.sha256(original).hexdigest()=='1b302ac2b21c2f21695e2989ddf8d2b30582691880fd935dbd6eec5b35f4ad77'
assert original[:4]==bytes.fromhex('cafebabe')
for index in range(struct.unpack_from('>I',original,4)[0]):
 cpu,sub,offset,size,align=struct.unpack_from('>IIIII',original,8+20*index)
 if cpu==0x01000007:
  (P/'loader.x64').write_bytes(original[offset:offset+size]);break
else:raise ValueError('x86_64 slice not found')
B=0x100000000; STOP=0x40000000; STK=0x70000000; HEAP=0x50000000
u=Uc(UC_ARCH_X86,UC_MODE_64); b=(P/'loader.x64').read_bytes();u.mem_map(B,0x200000)
cmdpos=32
for _ in range(struct.unpack_from('<I',b,16)[0]):
 cmd,size=struct.unpack_from('<II',b,cmdpos)
 if cmd==0x19:
  va,vs,fo,fs=struct.unpack_from('<QQQQ',b,cmdpos+24)
  if fs:u.mem_write(va,b[fo:fo+fs])
 cmdpos+=size
u.mem_map(STOP,0x10000);u.mem_map(STK,0x200000);u.mem_map(HEAP,0x8000000)
u.mem_write(B+0xfc380,struct.pack('<Q',HEAP));u.mem_write(B+0xfc388,struct.pack('<Q',HEAP+8));u.mem_write(HEAP,b'CANARY!!')
regs=[UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_RCX,UC_X86_REG_R8,UC_X86_REG_R9]
heap=HEAP+0x1000; known={}; api={}; onces=set(); phase='hash'
def alloc(n):
 global heap
 p=heap;heap+=(n+0xfff)&~0xfff;return p
def q(p): return struct.unpack('<Q',u.mem_read(p,8))[0]
def s(p):
 if not p:return b''
 x=bytearray()
 for i in range(2000000):
  c=u.mem_read(p+i,1)[0]
  if not c:break
  x.append(c)
 return bytes(x)
def ret(v=0):
 sp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RIP,q(sp));u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RAX,v&((1<<64)-1))
imports={B+0x82c5a:'bzero',B+0x82c60:'guard_acquire',B+0x82c66:'guard_release',B+0x82c6c:'FAIL',B+0x82c72:'free',B+0x82c78:'getpid',B+0x82c7e:'malloc',B+0x82c84:'memcpy',B+0x82c8a:'pthread_once',B+0x82c90:'strlen',B+0x82c96:'task_info',B+0x82c9c:'time'}
def hook(uc,a,z,data):
 global phase
 if a==STOP:uc.emu_stop();return
 if phase=='run' and a==B+0x80f20:
  v=[uc.reg_read(r) for r in regs];uc.mem_write(v[2],hashlib.sha256(bytes(uc.mem_read(v[0],v[1]))).digest());ret();return
 if phase=='run' and a==B+0x77190:
  v=[uc.reg_read(r) for r in regs];pw=bytes(uc.mem_read(v[0],36));salt=bytes(uc.mem_read(v[1],32));out=hashlib.pbkdf2_hmac('sha256',pw,salt,0x177e2,32);uc.mem_write(v[2],out);print('PBKDF2',pw.hex(),salt.hex(),out.hex(),flush=True);ret();return
 if phase=='run' and a in [B+x for x in [0x6f400,0x713a0,0x72bc0,0x74390,0x76a40]]:
  print('ANALYSIS assumption: no analysis trigger',hex(a),flush=True);ret(0);return
 if phase=='run' and a==B+0x7f860:
  h=uc.reg_read(UC_X86_REG_RDI);name=known.get(h,hex(h));ptr=STOP+0x100+len(api)*16;api[ptr]=name
  print('RESOLVE',hex(h),name,flush=True);ret(ptr);return
 name=imports.get(a,api.get(a))
 if name is None:return
 v=[uc.reg_read(r) for r in regs]
 if phase=='run':print('API',name,[hex(x) for x in v],flush=True)
 if name in ['malloc','calloc']:ret(alloc(v[0]*(v[1] if name=='calloc' else 1)))
 elif name in ['bzero','memset']:uc.mem_write(v[0],bytes([v[1]&255 if name=='memset' else 0])* (v[2] if name=='memset' else v[1]));ret(v[0])
 elif name in ['memcpy','memmove']:uc.mem_write(v[0],bytes(uc.mem_read(v[1],v[2])));ret(v[0])
 elif name=='CCCryptorGCMOneshotDecrypt':
  sp=uc.reg_read(UC_X86_REG_RSP);args=[q(sp+8*i) for i in range(1,7)];print('GCM',list(map(hex,args)),flush=True)
  key=bytes(uc.mem_read(v[1],v[2]));nonce=bytes(uc.mem_read(v[3],v[4]));ct=bytes(uc.mem_read(args[1],args[2]));tag=bytes(uc.mem_read(args[4],args[5]))
  try:
   plain=AESGCM(key).decrypt(nonce,ct+tag,None);uc.mem_write(args[3],plain);(P/('gcm-%04d.bin'%len(list(P.glob('gcm-*.bin'))))).write_bytes(plain);print('GCM OK',len(plain),flush=True);ret()
  except Exception as e:print('GCM FAILED',type(e).__name__,key.hex(),nonce.hex(),flush=True);ret(-1)
 elif name in ['objc_getClass','sel_registerName']:print('OBJC NAME',s(v[0]),flush=True);ret(v[0])
 elif name=='objc_msgSend':print('OBJC SEL',s(v[1]),flush=True);ret(1)
 elif name in ['pthread_main_np','OpenDefaultComponent']:ret(1)
 elif name in ['TransformProcessType','CloseComponent','AEDisposeDesc','OSADispose']:ret()
 elif name=='AECreateDesc':
  data=bytes(uc.mem_read(v[1],v[2]));(P/('osa-%d.scpt'%len(list(P.glob('osa-*.scpt'))))).write_bytes(data);uc.mem_write(v[3],struct.pack('<I4xQ',v[0],v[1]));print('OSA INPUT',len(data),flush=True);ret()
 elif name=='OSALoad':uc.mem_write(v[3],struct.pack('<I',1));ret()
 elif name=='OSAExecute':uc.mem_write(v[4],struct.pack('<I',1));ret()
 elif name=='strlen':ret(len(s(v[0])))
 elif name=='guard_release':uc.mem_write(v[0],b'\x01');ret()
 elif name=='free':ret()
 elif name=='guard_acquire':ret(1)
 elif name=='getpid':ret(1234)
 elif name=='time':ret(1792790000)
 elif name in ['mach_absolute_time','clock_gettime_nsec_np']:ret(1000000000)
 elif name in ['getuid','getgid','geteuid']:ret(501)
 elif name=='mmap':ret(alloc(v[1]))
 elif name in ['munmap','mprotect']:ret()
 elif name=='mach_timebase_info':uc.mem_write(v[0],struct.pack('<II',1,1));ret()
 elif name=='syscall':print('SYSCALL',v[0],bytes(uc.mem_read(v[1],16)).hex(),flush=True);ret(-1)
 elif name=='task_info':ret(-1)
 elif name=='proc_listpids':ret(0)
 elif name=='_dyld_get_image_header':ret(B)
 elif name=='getsectiondata':uc.mem_write(v[3],struct.pack('<Q',0x81ffa));ret(B+0xc60)
 elif name=='_dyld_image_count':ret(0)
 elif name=='gethostuuid':ret(-1)
 elif name in ['getppid','proc_selfpid']:ret(1)
 elif name=='proc_pidpath':uc.mem_write(v[1],b'/sbin/launchd\0');ret(13)
 elif name in ['setenv','unsetenv']:print('ENVWRITE',name,s(v[0]),s(v[1]) if name=='setenv' else '',flush=True);ret()
 elif name=='getenv':print('GETENV',s(v[0]),flush=True);ret()
 elif name=='dlopen':print('DLOPEN',s(v[0]),flush=True);ret(1)
 elif name=='dlsym':print('DLSYM',s(v[1]),flush=True);ret()
 elif name=='pthread_once' and v[0] in onces:ret()
 elif name=='pthread_once':
  onces.add(v[0])
  sp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,v[1])
 elif name=='sysctlbyname':print('SYSCTL',s(v[0]),flush=True);ret(0xffffffffffffffff)
 else:
  print('STOP UNKNOWN',name,'CALLER',hex(q(uc.reg_read(UC_X86_REG_RSP))),flush=True);uc.emu_stop()
u.hook_add(UC_HOOK_CODE,hook)
def run(addr,args=[]):
 u.reg_write(UC_X86_REG_RSP,STK+0x1fff00-8);u.mem_write(STK+0x1fff00-8,struct.pack('<Q',STOP))
 for r,v in zip(regs,args):u.reg_write(r,v)
 u.emu_start(B+addr,STOP+0x10000,count=200000000)
 return u.reg_read(UC_X86_REG_RAX)
for n in ['malloc','free','calloc','realloc','memset','memcpy','memmove','strlen','strcmp','strncmp','strstr','strchr','snprintf','sprintf','system','popen','pclose','fopen','fclose','fwrite','fread','fileno','fchmod','chmod','mkstemp','unlink','remove','getenv','setenv','unsetenv','getuid','getgid','geteuid','getpid','getppid','time','mach_absolute_time','clock_gettime_nsec_np','sysctl','sysctlbyname','ptrace','gettimeofday','dlopen','dlsym','CC_SHA256','CC_SHA256_Init','CC_SHA256_Update','CC_SHA256_Final','CCKeyDerivationPBKDF','CCCryptorGCM','CCCryptorGCMOneshotDecrypt','CCCryptorCreateWithMode','CCCryptorGCMAddIV','CCCryptorGCMAddAAD','CCCryptorGCMDecrypt','CCCryptorGCMFinal','CCCryptorRelease','CFUUIDCreate','CFUUIDCreateString','CFStringGetCString','CFRelease','objc_getClass','objc_msgSend','sel_registerName','NSCreateObjectFileImageFromMemory','NSLinkModule','NSLookupSymbolInModule','NSAddressOfSymbol','NSUnLinkModule','NSDestroyObjectFileImage','posix_spawn','execve','fork','exit','OpenDefaultComponent','OpenComponent','CloseComponent','AECreateDesc','AEDisposeDesc','AEGetDescDataSize','AEGetDescData','OSALoad','OSAExecute','OSADispose','OSACompile','OSADoScript','OSAGetScriptInfo','OSAGetDefaultScriptingComponent','OSAGetActiveProc','OSAGetScriptData','OSACopyID','OSADisplay','OSASetScriptInfo','OSAGetScriptError','GetDefaultComponent','dladdr','getprogname','pthread_main_np','objc_autoreleasePoolPush','objc_autoreleasePoolPop','Gestalt','NSApplicationLoad','IsMainThread','pthread_self','TransformProcessType','GetCurrentProcess','mmap','munmap','mprotect','mach_task_self','task_info','task_threads','thread_get_state','thread_info','mach_port_deallocate','mach_vm_region','vm_region_64','mach_timebase_info','getrusage','getpgrp','getdtablesize','proc_selfpid','proc_pidinfo','proc_listallpids','proc_listpids','sysctlnametomib','__getpid','getpgrp','_dyld_image_count','_dyld_get_image_name','_dyld_get_image_header','_dyld_get_image_vmaddr_slide','syscall','__sysctl','getsectiondata','SetFrontProcess','gethostuuid','sysconf','isatty','proc_pidpath','getppid','sysctlbyname','sysctl','csops','uname','stat']:
 p=HEAP+0x100;u.mem_write(p,('_'+n).encode()+b'\0'); h=run(0x80290,[p]);known[h]=n
phase='run'
try:run(0x6d500)
except UcError as e:print(e,'RIP',hex(u.reg_read(UC_X86_REG_RIP)))
assert u.reg_read(UC_X86_REG_RIP)==STOP, 'Emulation did not return normally'
main=max(P.glob('osa-*.scpt'),key=lambda f:f.stat().st_size).read_bytes()
assert len(main)==263770 and hashlib.sha256(main).hexdigest()=='3e629e744a04b3ffbe3e24863fd0f62212b7258e6cd611fc878fd2281458aa8b'
(P/'payload.scpt').write_bytes(main)
(P/'emulated-image.bin').write_bytes(bytes(u.mem_read(B,0x200000)))
(P/'emulated-stack.bin').write_bytes(bytes(u.mem_read(STK,0x200000)))
print('DONE RIP',hex(u.reg_read(UC_X86_REG_RIP)))
