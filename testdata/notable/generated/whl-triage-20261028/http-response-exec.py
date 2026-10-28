import requests

def run_remote(url):
    response=requests.get(url)
    source=response.json().get('code')
    exec(compile(source,'<remote>','exec'))
