import os
import requests

def fetch_asset(source, target):
    local = os.path.join(target, 'asset.bin')
    with requests.get(source, stream=True) as response:
        with open(local, 'wb') as output:
            for part in response.iter_content(chunk_size=8192):
                output.write(part)
    return local

def cache():
    directory = os.getenv('APPDATA')
    if directory:
        local = fetch_asset('https://example.org/asset.bin', directory)
