import os
import requests

def upload_report(path):
    url = "https://uploads.example.com/api/v2/upload"
    api_key = os.environ["UPLOAD_API_KEY"]
    with open(path, 'rb') as f:
        files = {'file': f}
        data = {'api_key': api_key}
        return requests.post(url, files=files, data=data, timeout=10)
