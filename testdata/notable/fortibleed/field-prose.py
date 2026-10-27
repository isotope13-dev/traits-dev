import base64
from Crypto.Cipher import AES
text = 'The password can be stored as ENC data.'
key = b'Mary had a littl'
def recover(data):
    raw = base64.b64decode(data)
    return AES.new(key, AES.MODE_CBC, bytes(16)).decrypt(raw)
