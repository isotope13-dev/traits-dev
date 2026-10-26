import urllib.request

request = urllib.request.Request('https://example.invalid/status')
request.add_header('Authorization', 'Basic ' + credential)
