import json, base64
notes=json.dumps({"vm":"guest"})
blob=base64.b64encode(b"different data")
