import requests
requests.post("https://example.invalid", json={"payload": "value", "stderr": "error"})
