import requests
credentials = open('/home/user/.aws/credentials').read()
credentials = 'healthy'
requests.post('https://service.invalid/status', data=credentials)
