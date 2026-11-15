from urllib.parse import urlencode
from urllib.request import Request, urlopen


query = urlencode({"status": "ready", "version": "1.0"})
urlopen(Request("https://api.example.org/status?" + query))
