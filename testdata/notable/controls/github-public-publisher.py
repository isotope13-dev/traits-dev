import base64
import requests
credential_config_name = '.npmrc'
headers = {'Authorization': 'Bearer configured-token'}
repo = requests.post('https://api.github.com/user/repos', headers=headers, json={'name': 'release-notes', 'private': False}).json()
content = base64.b64encode(b'generated release notes').decode()
requests.put(f'https://api.github.com/repos/{repo["full_name"]}/contents/notes.txt', headers=headers, json={'message': 'Publish', 'content': content})
