from pathlib import Path
import json, struct, hashlib
import pefile, capstone
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_EAX

p = next(Path('/var/tmp/qa/hostile').glob('bea*/*'))
b = p.read_bytes()
pe = pefile.PE(data=b)
base = pe.OPTIONAL_HEADER.ImageBase
u = Uc(UC_ARCH_X86, UC_MODE_32)
u.mem_map(base, (pe.OPTIONAL_HEADER.SizeOfImage+4095)&~4095)
u.mem_write(base, pe.get_memory_mapped_image())
u.mem_map(0x20000000, 0x200000)
u.mem_map(0x70000000, 0x200000)
u.reg_write(UC_X86_REG_ESP, 0x70100000)
u.reg_write(UC_X86_REG_EBP, 0x70110000)
u.mem_write(0x70100000, struct.pack('<I', 0x70001000))
u.mem_write(0x5052e0, struct.pack('<I', 0x20000000))
stops=[]
def code(uc, at, size, user):
    # Only the statically reviewed byte-reconstruction function may run.
    # Its output and all imports/application code remain unexecuted.
    if not 0x501042 <= at < 0x5011ba:
        stops.append({'reason':'routine boundary','at':hex(at)})
        uc.emu_stop()
def invalid(uc, access, at, size, value, user):
    stops.append({'reason':'unmapped','ip':hex(uc.reg_read(UC_X86_REG_EIP)),'address':hex(at)})
    return False
u.hook_add(UC_HOOK_CODE,code)
u.hook_add(UC_HOOK_MEM_INVALID,invalid)
try:
    u.emu_start(0x501042, 0x70001000, count=2_000_000, timeout=5_000_000)
except UcError as e:
    stops.append({'reason':'emulator error','error':str(e)})
mem=bytes(u.mem_read(0x20000000,0x10000))
Path('/tmp/hostile-triage/bea-fragment-buffer.bin').write_bytes(mem)
info={'sample_sha256':hashlib.sha256(b).hexdigest(),'stops':stops,'ip':hex(u.reg_read(UC_X86_REG_EIP)),
      'eax':hex(u.reg_read(UC_X86_REG_EAX)),
      'globals':{hex(a):hex(struct.unpack('<I',u.mem_read(a,4))[0]) for a in [0x50509a,0x50509e,0x5052e0,0x5052f0]},
      'buffer_sha256':hashlib.sha256(mem).hexdigest()}
Path('/tmp/hostile-triage/bea-fragment-reconstruction.json').write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps(info,indent=2))
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
for at in [0,struct.unpack('<I',u.mem_read(0x50509e,4))[0]-0x20000000]:
    if 0<=at<len(mem):
        print('OUTPUT',hex(at),mem[at:at+40].hex(' '))
        for x in list(cs.disasm(mem[at:at+200],0x20000000+at))[:40]:print(hex(x.address),x.mnemonic,x.op_str)
