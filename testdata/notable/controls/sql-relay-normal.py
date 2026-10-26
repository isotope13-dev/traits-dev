import urllib.request
url = "https://relay.example/fetch?url=https%3A%2F%2Frecords.example%2FRecord?record=7"
with urllib.request.urlopen(url) as response:
    print(response.status)
# https://relay.example/fetch?url=https://records.example/Record?record=1+OR+1%3D1
