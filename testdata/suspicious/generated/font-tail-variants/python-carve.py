import base64
from pathlib import Path
blob = Path('Display-Regular.woff').read_bytes()
payload = base64.b64decode(blob.split(b'%%BOUNDARY%%', 1)[1])
Path('decoded.bin').write_bytes(payload)
