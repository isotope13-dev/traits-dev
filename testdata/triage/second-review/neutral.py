import requests
from concurrent.futures import ThreadPoolExecutor
url = 'http://116.202.0.1:11434'
resp = requests.get(f'{url}/api/tags')
with ThreadPoolExecutor(max_workers=2) as pool:
    pass
requests.post(f'{url}/v1/chat/completions', json={'messages': []})
