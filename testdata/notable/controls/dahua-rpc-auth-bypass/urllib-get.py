from urllib.request import Request, urlopen
data = b"body"
urlopen(Request("https://example.org", data=data, headers={}, method="GET"))
