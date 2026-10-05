import requests

response = requests.get("https://example.invalid/api/records?State_Id=1+OR+1%3D1")
print(response.status_code)
