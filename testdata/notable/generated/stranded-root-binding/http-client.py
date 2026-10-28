import requests
response = requests.get("https://example.org/status")
response.raise_for_status()
