import urllib.request
import urllib.parse
body = urllib.parse.urlencode({'wanMode': '2', 'pppUserName': 'customer@example.net', 'submit-url': '/wan.asp'}).encode()
request = urllib.request.Request('http://router.invalid/goform/setWAN', data=body, method='POST')
