import requests
resp = requests.post("https://login.microsoftonline.com/common/oauth2/token", data={"grant_type": "password", "username": user, "password": password})
result = resp.json()
if result:
    records.append((user, password, result["refresh_token"]))
