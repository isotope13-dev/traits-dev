
import hashlib, os, sys, winreg
def _guid():
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Cryptography')
    v, _ = winreg.QueryValueEx(k, 'MachineGuid')
    return v
marker = hashlib.sha256(_guid().encode()).hexdigest()
here = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(here, marker)):
    sys.exit(0)
print("licensed")
