import base64
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def recover(config):
    for entry in re.finditer(r'set (?:password|passwd) ENC (\S+)', config):
        raw = base64.b64decode(entry.group(1))
        decryptor = Cipher(algorithms.AES(b'Mary had a littl'),
                           modes.CBC(raw[:4] + bytes(12))).decryptor()
        yield (decryptor.update(raw[4:]) + decryptor.finalize()).split(b'\0')[0]
