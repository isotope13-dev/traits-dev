import requests
requests.post("https://example.invalid/tenant/admin%42/run", data=b"probe")
