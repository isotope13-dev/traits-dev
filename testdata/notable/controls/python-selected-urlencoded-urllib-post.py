import os
import urllib.parse
import urllib.request

environment = {"language": os.environ.get("LANG", "en")}
body = urllib.parse.urlencode(environment).encode()
request = urllib.request.Request("https://service.example/", data=body)
urllib.request.urlopen(request)
