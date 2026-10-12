import urllib.request
req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=b"{}")
with urllib.request.urlopen(req) as response:
    body = response.read()
