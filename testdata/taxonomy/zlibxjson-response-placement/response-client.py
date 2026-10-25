import requests
response = requests.get("https://example.com/status")
response.raise_for_status()
