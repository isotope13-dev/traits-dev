import os
import requests

def list_files():
    runner = os.environ.get('RUNNER_NAME')
    return runner, requests.get('https://www.googleapis.com/drive/v3/files/')
