import requests
r = requests.get("https://example.org/data", stream=True)
for chunk in r.iter_content(8192):
    print(len(chunk))
