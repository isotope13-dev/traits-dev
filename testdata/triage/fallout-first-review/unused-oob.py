import urllib.request
DOCUMENTATION = "https://webhook.site/3ed49781-633a-4d15-a259-bb961c765db4"
try:
    urllib.request.urlopen("https://example.org/status", timeout=2)
except Exception:
    pass
