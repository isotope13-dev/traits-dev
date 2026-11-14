import requests

response = requests.get('https://github.com/example/tool/releases/download/v1.0/tool.tar.gz')
print(response.status_code)
