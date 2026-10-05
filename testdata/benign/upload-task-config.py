import json
import urllib.request

fields = {'copyTo': '/srv/tasks'}
payload = {'meta': {'name': 'daily-report'}}
req = urllib.request.Request('https://example.invalid/FileUpload',
                             data=json.dumps(payload).encode(), method='POST')
