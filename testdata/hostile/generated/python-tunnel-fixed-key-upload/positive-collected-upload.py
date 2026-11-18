import requests

def upload_file(path):
    url = "https://example-collect-92.telebit.io/api/v2/upload"
    api_key = "GROUP_USERS"
    with open(path, 'rb') as f:
        files = {'file': f}
        data = {'api_key': api_key}
        return requests.post(url, files=files, data=data, timeout=10)
