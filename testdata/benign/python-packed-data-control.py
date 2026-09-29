"""Unpack a static, non-executable resource table."""

import base64
import gzip

RESOURCE = "H4sIAAAAAAAC/0rOzy0oSi0uTkxPVShJLS5OTE8FAJzXgOcNAAAA"
RESOURCE_TEXT = gzip.decompress(base64.b64decode(RESOURCE)).decode("utf-8")
LABELS = RESOURCE_TEXT.splitlines()
