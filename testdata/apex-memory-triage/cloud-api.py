import urllib.request
req = urllib.request.Request("https://ollama.com/api/chat", data=b"{}")
with urllib.request.urlopen(req) as response:
    body = response.read()
