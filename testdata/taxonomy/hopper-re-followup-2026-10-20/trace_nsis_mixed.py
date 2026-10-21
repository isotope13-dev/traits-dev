"""Conditional CPU-only x64 continuation with synthetic TEBs/PEBs/ntdll."""
import argparse,runpy,sys,struct,json,time,collections
from pathlib import Path
import unicorn,capstone
from unicorn.x86_const import *
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--audit-root',type=Path,required=True)
ap.add_argument('--output-dir',type=Path,required=True)
ap.add_argument('--model-window-count',type=int,choices=range(65),default=None)
ap.add_argument('--assume-thread-hide-success',action='store_true')
args=ap.parse_args()
model=Path(__file__).with_name('trace_nsis_stage.py')
sys.argv=[str(model),'--audit-root',str(args.audit_root),'--output-dir',str(args.output_dir),'--assume-no-memory-marker','--model-mapped-memory','--model-resolver-state']
if args.model_window_count is not None:sys.argv+=['--model-window-count',str(args.model_window_count)]
if args.assume_thread_hide_success:sys.argv+=['--assume-thread-hide-success']
g=runpy.run_path(str(model));old=g['u'];stage=g['stage'];out=g['output'];u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
assert old.reg_read(UC_X86_REG_EIP)==stage+0x1c995
entry,selector=struct.unpack('<IH',old.mem_read(old.reg_read(UC_X86_REG_EAX),6))
assert selector==0x33 and entry==stage+0x1c9a2
for start,end,perm in old.mem_regions():
 u.mem_map(start,end-start+1,perm);u.mem_write(start,bytes(old.mem_read(start,end-start+1)))
regs=['AX','BX','CX','DX','SI','DI','SP','BP']
for name in regs:u.reg_write(globals()['UC_X86_REG_R'+name],old.reg_read(globals()['UC_X86_REG_E'+name]))
u.reg_write(UC_X86_REG_EFLAGS,old.reg_read(UC_X86_REG_EFLAGS))
u.mem_map(0x50000000,0x100000)
u.reg_write(UC_X86_REG_FS_BASE,0x50000000);u.reg_write(UC_X86_REG_GS_BASE,0x50010000)
def w32(a,x):u.mem_write(a,struct.pack('<I',x))
def w64(a,x):u.mem_write(a,struct.pack('<Q',x))
w64(0x50000018,0x50000000);w32(0x50000030,0x50020000);w32(0x500200a4,10)
w64(0x50010030,0x50010000);w64(0x50010060,0x50030000);w64(0x50030018,0x50040000)
w64(0x50040020,0x50050000);w64(0x50050000,0x50051000);w64(0x50051020,0x50060000)
w32(0x5006003c,0x100);w32(0x50060138,0x1000);w32(0x50060218,0x1000)
u.mem_write(0x50061000,b'\x90'*0x1000)
last=collections.deque(maxlen=40);events=[];count=0;started=time.monotonic();c=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
class Stop(Exception):pass
def hook(uc,a,n,x):
 global count
 count+=1;last.append(a-stage)
 if count>1000000 or time.monotonic()-started>30:raise Stop('budget')
 op=bytes(u.mem_read(a,min(n,15)))
 if op[:2]==b'\x0f\x05':
  events.append({'syscall':hex(u.reg_read(UC_X86_REG_RAX)),'pc':hex(a-stage),'rcx':hex(u.reg_read(UC_X86_REG_RCX)),'rdx':hex(u.reg_read(UC_X86_REG_RDX)),'r8':hex(u.reg_read(UC_X86_REG_R8)),'r9':hex(u.reg_read(UC_X86_REG_R9))})
  if u.reg_read(UC_X86_REG_RAX)!=0x50:raise Stop('unmodeled syscall')
  events[-1]['assumption']='NtProtectVirtualMemory succeeds against the synthetic ntdll image'
  u.reg_write(UC_X86_REG_RAX,0);u.reg_write(UC_X86_REG_RIP,a+2)
 if not stage<=a<stage+len(g['code']):raise Stop('outside stage')
u.hook_add(unicorn.UC_HOOK_CODE,hook)
try:u.emu_start(entry,stage+len(g['code']),timeout=30000000,count=1000000);reason='end or budget'
except Exception as e:reason=str(e)
res={'reason':reason,'instructions':count,'events':events,'rip':hex(u.reg_read(UC_X86_REG_RIP)-stage),'last':[hex(x) for x in last],'registers':{n:hex(u.reg_read(globals()['UC_X86_REG_R'+n])) for n in regs}}
(out/'trace64.json').write_text(json.dumps(res,indent=2));(out/'stack64.bin').write_bytes(bytes(u.mem_read(0x20000000,0x200000)))
print(json.dumps(res,indent=2))
# Resume the x86 continuation only after validating the modeled far return.
assert u.reg_read(UC_X86_REG_RIP)==stage+0x1d13f
ptr=u.reg_read(UC_X86_REG_RCX);target,selector=struct.unpack('<IH',u.mem_read(ptr,6));assert selector==0x23 and target==stage+0x1c99c
for start,end,perm in old.mem_regions():old.mem_write(start,bytes(u.mem_read(start,end-start+1)))
# Supply explicit synthetic Windows structures to resumed x86 code.
# FS has zero base in this 32-bit model, so [FS:30] is backed at address 0x30.
old.mem_map(0x50000000,0x100000);old.mem_write(0x50000000,bytes(u.mem_read(0x50000000,0x100000)))
if not any(start==0 for start,end,perm in old.mem_regions()):old.mem_map(0,0x1000)
def old32(a,x):old.mem_write(a,struct.pack('<I',x))
old32(0x18,0x50000000);old32(0x30,0x50020000);old32(0x5002000c,0x50070000)
# A synthetic installer invocation, not an observed launch command. The stage
# reads ProcessParameters.CommandLine.Buffer via [PEB+10]+44; leaving this
# pointer null incorrectly turns environment access into an obfuscation fault.
old32(0x50020010,0x50090000)
def old_unicode(structure, address, value):
    encoded=value.encode('utf-16le')
    old.mem_write(structure,struct.pack('<HHI',len(encoded),len(encoded)+2,address))
    old.mem_write(address,encoded+b'\0\0')
old_unicode(0x50090038,0x50092000,r'C:\triage\RFQ Fabrics.exe')
old_unicode(0x50090040,0x50093000,r'"C:\triage\RFQ Fabrics.exe"')
old32(0x50090048,0x50094000)

old32(0x50070014,0x50071000);old32(0x50071000,0x50072000);old32(0x50072010,0x50080000)
old32(0x5008003c,0x100);old32(0x5008012c,0x1000);old32(0x50080208,0x1000)
old.mem_write(0x50081000,b'\x90'*0x1000)
for name in regs:old.reg_write(globals()['UC_X86_REG_E'+name],u.reg_read(globals()['UC_X86_REG_R'+name])&0xffffffff)
old.reg_write(UC_X86_REG_EFLAGS,u.reg_read(UC_X86_REG_EFLAGS));old.reg_write(UC_X86_REG_EIP,target)
env=g['hook'].__globals__;env['started']=time.monotonic();env['events'].append({'assumption':'x64 continuation uses synthetic Windows 10 TEB/PEB/module metadata and a NOP-filled ntdll text section; protection syscall returns success; resumed x86 uses synthetic PEB/Ldr/PE headers and NOP text','synthetic_command_line':r'"C:\triage\RFQ Fabrics.exe"','x64_instructions':count,'return_to_x86':hex(target-stage)})
g['run_trace']()
