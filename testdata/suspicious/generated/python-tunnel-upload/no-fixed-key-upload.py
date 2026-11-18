import requests

def send_report(path, token):
    url = "https://demo-share-17.serveo.net/upload"
    with open(path, 'rb') as f:
        files = {'file': f}
        return requests.post(url, files=files, headers={'Authorization': token}, timeout=10)
