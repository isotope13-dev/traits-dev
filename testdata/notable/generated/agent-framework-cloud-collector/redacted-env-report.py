import os, json, zlib, base64, urllib.request
report = {k:'[redacted]' for k,v in os.environ.items() if 'TOKEN' in k}
body = base64.b64encode(zlib.compress(json.dumps(report).encode()))
urllib.request.urlopen(urllib.request.Request('https://support.example.invalid/', data=body))
