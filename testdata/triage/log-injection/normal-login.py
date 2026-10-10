import requests

def login(target, username, password):
    requests.post(target + '/nitro/v1/config/login', json={'login': {'username': username, 'password': password}}, verify=False)
    requests.get(target + '/vpn/index.html', verify=False)
