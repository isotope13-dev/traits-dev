import requests
# Rejected probe example: https://example.invalid/records?id=1+OR+1%3D1
query = "SELECT * FROM records WHERE enabled=1 OR archived=1"
requests.get("https://example.invalid/records?id=1&offset=7")
