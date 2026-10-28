import requests

def get_status(url):
    response=requests.get(url)
    data=response.json()
    return data.get('code')

def run_local(source):
    exec(compile(source,'<local>','exec'))
