import os
import requests

def transfer(source, destination):
    saved = os.path.join('/tmp', 'asset.bin')
    with requests.get(source, stream=True) as response:
        with open(saved, 'wb') as output:
            for part in response.iter_content(chunk_size=8192):
                output.write(part)
    return saved

def cache():
    root = os.getenv('APPDATA')
    if root:
        saved = transfer('https://example.org/asset.bin', root)
