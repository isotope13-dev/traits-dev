import requests

def read_catalog():
    for object_id in range(200):
        response = requests.get(f"https://catalog.corpus.invalid/api?id={object_id}", timeout=10)
        response.raise_for_status()
        yield response.json()
