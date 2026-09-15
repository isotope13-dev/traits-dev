import requests
credentials = open('/home/user/.aws/credentials').read()
requests.get('https://service.invalid/status')
