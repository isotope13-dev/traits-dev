import marshal
from Crypto.Cipher import ChaCha20
clear = ChaCha20.new(key=key, nonce=nonce).decrypt(blob)
save_report(clear)
exec(marshal.loads(other_blob))
