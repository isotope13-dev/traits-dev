import urllib.request
url = 'https://example.org/api/status/ordinary-session'
with urllib.request.urlopen(url) as response:
    print(response.status)
# A comment showing /api/status/%27%3Bid%3Becho%20%27 is not executable data.
