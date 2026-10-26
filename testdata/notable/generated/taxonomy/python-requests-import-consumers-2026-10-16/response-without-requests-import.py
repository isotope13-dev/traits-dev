from urllib.request import urlopen
response = urlopen("https://example.invalid/payload")
body = response.content
