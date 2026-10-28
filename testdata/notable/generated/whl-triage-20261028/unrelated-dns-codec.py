import base64, subprocess, requests

def encode_config(config):
    return base64.urlsafe_b64encode(config).decode()

def lookup(domain):
    return subprocess.run(['nslookup', domain])

def batches(data, n):
    return [data[i:i+n] for i in range(0, len(data), n)]

def fetch_page(url):
    return requests.get(url)
