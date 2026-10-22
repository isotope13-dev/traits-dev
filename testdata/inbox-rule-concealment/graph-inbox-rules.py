import os
import requests

session = requests.Session()
session.headers['Authorization'] = 'Bearer ' + os.environ['ACCESS_TOKEN']
endpoint = 'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules'
folder = session.get('https://graph.microsoft.com/v1.0/me/mailFolders',
    params={'$filter': "displayName eq 'Conversation History'"}).json()['value'][0]['id']
rules = [
    {'displayName': 'sss', 'sequence': 1, 'isEnabled': True,
     'conditions': {}, 'actions': {'markAsRead': True, 'delete': True}},
    {'displayName': 'iT', 'sequence': 2, 'isEnabled': True,
     'conditions': {}, 'actions': {'moveToFolder': folder, 'markAsRead': True}}
]
for rule in rules:
    session.post(endpoint, json=rule).raise_for_status()
