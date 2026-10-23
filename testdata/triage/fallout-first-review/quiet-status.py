# A diagnostic callback with no local source data.
import urllib.request
try:
    urllib.request.urlopen("https://webhook.site/3ed49781-633a-4d15-a259-bb961c765db4", timeout=2)
except Exception:
    pass
