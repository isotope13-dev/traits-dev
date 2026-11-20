import requests
payload = {"scope": "applied-permissions/admin", "audience": "*", "expires_in": 3600}
requests.post("https://admin.example.invalid/access/api/v1/tokens", data=payload)
