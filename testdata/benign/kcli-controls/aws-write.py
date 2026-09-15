import urllib.request
with open('/home/user/.aws/credentials', 'w') as f:
    f.write('aws_access_key_id=x\naws_secret_access_key=y')
urllib.request.urlopen('https://service.invalid/status')
