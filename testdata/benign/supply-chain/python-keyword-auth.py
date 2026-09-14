# Static analysis fixture. Do not execute. Header authentication is not body exfiltration.
import os
import requests
if False:
    requests.post('https://service.example.invalid/status', headers={'Authorization': os.getenv('DEPLOY_API_KEY')}, json={'status': 'ready'})
