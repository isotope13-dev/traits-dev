import json, base64
notes = base64.b64encode(json.dumps({"vm":"guest"}).encode()).decode()
