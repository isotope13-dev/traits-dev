import requests
response = requests.get("https://example.invalid/payload")
body = response.content
