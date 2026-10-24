import requests
client_id = "application-id"
response = requests.post(
    'https://login.microsoftonline.com/organizations/oauth2/v2.0/token',
    data={'grant_type': 'password', 'client_id': client_id,
          'username': username, 'password': password,
          'scope': 'https://graph.microsoft.com/.default'}, timeout=20)
print(response.status_code)
