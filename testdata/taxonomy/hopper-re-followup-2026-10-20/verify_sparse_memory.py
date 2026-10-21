"""Exercise sparse-model cross-page accesses, bounds, zero fill and no-execute."""
import json
import runpy
import struct
from pathlib import Path
import unicorn
from unicorn.x86_const import UC_X86_REG_EAX

SparseReservation = runpy.run_path(str(Path(__file__).with_name('trace_nsis_allocation.py')))['SparseReservation']
uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
uc.mem_map(0x1000, 4096)
r = SparseReservation(uc, 0x100000, 0x3000, max_backed=8192)
# A zero-filled page read, followed by a dword straddling a page boundary.
code = b'\xa1'+struct.pack('<I',0x100100)
uc.mem_write(0x1000,code); uc.emu_start(0x1000,0x1000+len(code),count=2)
assert uc.reg_read(UC_X86_REG_EAX)==0
code = b'\xc7\x05'+struct.pack('<II',0x100fff,0x12345678)+b'\xa1'+struct.pack('<I',0x100fff)
uc.mem_write(0x1000,code); uc.emu_start(0x1000,0x1000+len(code),count=3)
assert uc.reg_read(UC_X86_REG_EAX)==0x12345678 and len(r.pages)==2
# The third page would exceed the backing cap.
uc.mem_write(0x1000,b'\xa1'+struct.pack('<I',0x102000))
try: uc.emu_start(0x1000,0x1005,count=2)
except unicorn.UcError as e: assert e.errno==unicorn.UC_ERR_READ_UNMAPPED
else: raise AssertionError('backing cap bypassed')
assert r.limit_reached and len(r.pages)==2
for address, expected in [(0x100000,unicorn.UC_ERR_FETCH_PROT),(0x102000,unicorn.UC_ERR_FETCH_UNMAPPED)]:
    try: uc.emu_start(address,address+1,count=1)
    except unicorn.UcError as e: assert e.errno==expected
    else: raise AssertionError('execution allowed in data reservation')
assert not r.fault(uc,unicorn.UC_MEM_WRITE_UNMAPPED,0x102fff,4,0,None)
assert len(r.pages)==2
try: SparseReservation(uc,0x100000,4096)
except AssertionError: pass
else: raise AssertionError('overlap accepted')
print(json.dumps({'verified':['zero-filled read','cross-page write/read','backing cap','mapped no-execute','unmapped no-execute','reservation boundary','overlap rejection']}))
