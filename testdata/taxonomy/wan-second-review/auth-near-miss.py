import urllib.request

request = urllib.request.Request('https://example.invalid/status')
request.add_header('Authorization', 'Bearer ' + token)
label = 'Basic ' + caption
unrelated = {'description': 'Basic ' + encoded}
