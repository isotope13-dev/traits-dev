import base64
from Crypto.Cipher import AES
key = b"Mary had a littl"
pattern = r"set password ENC"
backup_path = "/api/v2/monitor/system/config/backup"
raw = base64.b64decode(saved_enc)
