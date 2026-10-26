import base64
from pathlib import Path

font = Path("Display-Regular.woff").read_bytes()
print(base64.b64encode(font).decode())
