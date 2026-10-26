import json
import urllib.request

def report(url, user, password, endpoint):
    record = {"url": url, "user": user, "password": password}
    if endpoint:
        request = urllib.request.Request(endpoint, data=json.dumps(record).encode("utf-8"), method="POST")
        urllib.request.urlopen(request)
